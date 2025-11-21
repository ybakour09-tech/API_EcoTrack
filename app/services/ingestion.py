from __future__ import annotations

from datetime import datetime
from typing import Iterable

import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.indicator import Indicator
from app.models.source import Source
from app.models.zone import Zone

# Endpoints OpenAQ v3
OPENAQ_V3_LOCATIONS = "https://api.openaq.org/v3/locations"
OPENAQ_URL = OPENAQ_V3_LOCATIONS


def fetch_openaq(
    limit: int = 10,
    city: str | None = None,
    country: str | None = None,
    location_id: int | None = None,
) -> list[dict]:
    """
    Récupère des mesures via OpenAQ v3.

    - Si location_id est fourni :
        -> /v3/locations/{id}
        -> /v3/locations/{id}/sensors
        -> /v3/sensors/{sensor_id}/measurements?limit=...
        => renvoie plusieurs valeurs (historique) pour cette localisation.

    - Sinon :
        -> /v3/locations (filtré éventuellement par iso=country)
        -> filtre Python sur city (name/locality/owner/provider)
        -> /v3/locations/{id}/latest
        => snapshot (une valeur récente par capteur).
    """
    if not settings.openaq_api_key:
        raise HTTPException(
            503,
            detail=(
                "OPENAQ_API_KEY n'est pas défini. "
                "Configurez une clé API OpenAQ pour utiliser la v3."
            ),
        )

    headers = {"X-API-Key": settings.openaq_api_key}

    # ------------- CAS 1 : location_id fourni -> historique par capteur -------------
        # ------------- CAS 1 : location_id fourni -> historique par capteur + fallback /latest -------------
    if location_id is not None:
        # Infos de la localisation
        try:
            resp_loc = httpx.get(
                f"{OPENAQ_V3_LOCATIONS}/{location_id}",
                headers=headers,
                timeout=20,
            )
            resp_loc.raise_for_status()
        except httpx.HTTPError as exc:
            raise HTTPException(
                503,
                detail=f"OpenAQ v3 non accessible (location {location_id}): {exc}",
            ) from exc

        loc_payload = resp_loc.json()
        loc_results = loc_payload.get("results")
        if isinstance(loc_results, list) and loc_results:
            loc = loc_results[0]
        else:
            loc = loc_payload

        loc_name = loc.get("name")
        loc_city = loc.get("locality") or (
            (loc.get("country") or {}).get("name")
            if isinstance(loc.get("country"), dict)
            else None
        )
        loc_coords = loc.get("coordinates")

        # Récupérer les capteurs de cette localisation
        try:
            resp_sensors = httpx.get(
                f"{OPENAQ_V3_LOCATIONS}/{location_id}/sensors",
                headers=headers,
                timeout=20,
            )
            resp_sensors.raise_for_status()
        except httpx.HTTPError as exc:
            raise HTTPException(
                503,
                detail=f"OpenAQ v3 non accessible (sensors location {location_id}): {exc}",
            ) from exc

        sensors_payload = resp_sensors.json()
        sensors = sensors_payload.get("results", []) or []

        meas_list: list[dict] = []

        # 1) Essai historique par capteur
        for sensor in sensors:
            sensor_id = sensor.get("id")
            if sensor_id is None:
                continue

            try:
                resp_meas = httpx.get(
                    f"https://api.openaq.org/v3/sensors/{sensor_id}/measurements",
                    headers=headers,
                    params={"limit": limit},
                    timeout=20,
                )
                resp_meas.raise_for_status()
            except httpx.HTTPError:
                # On ignore ce capteur en cas d'erreur
                continue

            meas_payload = resp_meas.json()
            for row in meas_payload.get("results", []) or []:
                dt_struct = row.get("datetime")
                if isinstance(dt_struct, dict):
                    dt = dt_struct.get("utc")
                else:
                    dt = dt_struct
                if not dt:
                    continue

                meas_list.append(
                    {
                        "parameter": row.get("parameter"),
                        "value": row.get("value"),
                        "unit": row.get("unit"),
                        "lastUpdated": dt,
                    }
                )

        # 2) Fallback : si aucune mesure via /sensors/{id}/measurements,
        #    on repasse sur /locations/{id}/latest comme avant.
        if not meas_list:
            try:
                resp_latest = httpx.get(
                    f"{OPENAQ_V3_LOCATIONS}/{location_id}/latest",
                    headers=headers,
                    params={"limit": limit},
                    timeout=20,
                )
                resp_latest.raise_for_status()
            except httpx.HTTPError as exc:
                raise HTTPException(
                    404,
                    detail=f"Aucune mesure OpenAQ pour location_id={location_id}.",
                ) from exc

            latest_payload = resp_latest.json()
            latest_results = latest_payload.get("results", []) or []

            for row in latest_results:
                dt_struct = row.get("datetime")
                if isinstance(dt_struct, dict):
                    dt = dt_struct.get("utc")
                else:
                    dt = dt_struct
                if not dt:
                    continue

                meas_list.append(
                    {
                        "parameter": row.get("parameter"),
                        "value": row.get("value"),
                        "unit": row.get("unit"),
                        "lastUpdated": dt,
                    }
                )

        if not meas_list:
            raise HTTPException(
                404,
                detail=f"Aucune mesure OpenAQ pour location_id={location_id}.",
            )

        return [
            {
                "location": loc_name,
                "city": loc_city,
                "coordinates": loc_coords,
                "measurements": meas_list,
            }
        ]


    # ------------- CAS 2 : pas de location_id -> snapshot via /latest -------------
    # 1) Récupérer une liste de locations
    params_locations: dict[str, object] = {"limit": limit}
    if country:
        # filtre pays : iso=FR, iso=US, etc.
        params_locations["iso"] = country

    try:
        resp_locations = httpx.get(
            OPENAQ_V3_LOCATIONS,
            params=params_locations,
            headers=headers,
            timeout=20,
        )
        resp_locations.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(
            503,
            detail=f"OpenAQ v3 non accessible (locations): {exc}",
        ) from exc

    locations_payload = resp_locations.json()
    locations = locations_payload.get("results", []) or []

    # Filtre "city" en Python (name/locality/owner/provider)
    if city:
        needle = city.lower()
        filtered: list[dict] = []
        for loc in locations:
            name = (loc.get("name") or "").lower()
            locality = (loc.get("locality") or "").lower()
            owner_name = ((loc.get("owner") or {}).get("name") or "").lower()
            provider_name = ((loc.get("provider") or {}).get("name") or "").lower()
            if (
                needle in name
                or needle in locality
                or needle in owner_name
                or needle in provider_name
            ):
                filtered.append(loc)
        if filtered:
            locations = filtered

    if not locations:
        raise HTTPException(
            404,
            detail=(
                f"Aucune location OpenAQ ne correspond à ces filtres "
                f"(city={city}, country={country}, location_id={location_id}). "
                "Vérifiez les valeurs renvoyées par /v3/locations."
            ),
        )

    measurements: list[dict] = []

    # 2) Pour chaque location -> /v3/locations/{id}/latest (snapshot)
    for loc in locations[:limit]:
        loc_id = loc.get("id")
        if loc_id is None:
            continue

        try:
            resp_latest = httpx.get(
                f"{OPENAQ_V3_LOCATIONS}/{loc_id}/latest",
                headers=headers,
                params={"limit": limit},
                timeout=20,
            )
            resp_latest.raise_for_status()
        except httpx.HTTPError:
            continue

        latest_payload = resp_latest.json()
        latest_results = latest_payload.get("results", []) or []

        meas_list_loc: list[dict] = []
        for row in latest_results:
            dt_struct = row.get("datetime")
            if isinstance(dt_struct, dict):
                dt = dt_struct.get("utc")
            else:
                dt = dt_struct
            if not dt:
                continue

            meas_list_loc.append(
                {
                    "parameter": row.get("parameter"),
                    "value": row.get("value"),
                    "unit": row.get("unit"),
                    "lastUpdated": dt,
                }
            )

        if not meas_list_loc:
            continue

        measurements.append(
            {
                "location": loc.get("name"),
                "city": loc.get("locality") or ((loc.get("country") or {}).get("name")),
                "coordinates": loc.get("coordinates"),
                "measurements": meas_list_loc,
            }
        )

    if not measurements:
        raise HTTPException(
            404,
            detail=(
                f"Aucune donnée OpenAQ ne correspond à ces filtres "
                f"(city={city}, country={country}, location_id={location_id}). "
                "Vérifiez les valeurs exactes renvoyées par /v3/locations."
            ),
        )

    return measurements


def upsert_source(db: Session, name: str, description: str, url: str) -> Source:
    source = db.query(Source).filter_by(name=name).first()
    if not source:
        source = Source(name=name, description=description, url=url)
        db.add(source)
        db.commit()
        db.refresh(source)
    return source


def get_or_create_zone(db: Session, *, name: str, postal_code: str | None = None) -> Zone:
    query = db.query(Zone).filter(Zone.name == name)
    if postal_code:
        query = query.filter(Zone.postal_code == postal_code)
    zone = query.first()
    if not zone:
        zone = Zone(name=name, postal_code=postal_code)
        db.add(zone)
        db.commit()
        db.refresh(zone)
    return zone


def save_measurements(
    db: Session,
    measurements: Iterable[dict],
    *,
    indicator_type: str = "pm25",
):
    source = upsert_source(
        db,
        name="OpenAQ",
        description="API qualité de l'air OpenAQ",
        url=OPENAQ_URL,
    )
    created = 0
    for result in measurements:
        location = result.get("location")
        postal_code = result.get("city")
        zone = get_or_create_zone(
            db,
            name=location or postal_code or "Unknown",
            postal_code=postal_code,
        )

        for measurement in result.get("measurements", []):
            last_updated = measurement.get("lastUpdated")
            if not last_updated:
                continue

            # fallback robuste pour le type et l'unité
            param = measurement.get("parameter") or indicator_type
            unit = measurement.get("unit") or "µg/m3"

            ts = datetime.fromisoformat(last_updated.replace("Z", "+00:00"))
            indicator = Indicator(
                type=param,
                value=measurement.get("value"),
                unit=unit,
                timestamp=ts,
                zone_id=zone.id,
                source_id=source.id,
                payload={
                    "location": location,
                    "coordinates": result.get("coordinates"),
                },
            )
            db.add(indicator)
            created += 1

    db.commit()
    return created
