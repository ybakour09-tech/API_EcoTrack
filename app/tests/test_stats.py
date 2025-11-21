from datetime import datetime, timezone

from fastapi.testclient import TestClient


def authenticate(client: TestClient, email: str, password: str) -> str:
    response = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return response.json()["token"]["access_token"]


def seed_indicator(client: TestClient, headers: dict):
    zone = client.post("/api/v1/zones/", json={"name": "Zone Stats"}, headers=headers).json()
    source = client.post(
        "/api/v1/sources/", json={"name": "Source Stats"}, headers=headers
    ).json()
    client.post(
        "/api/v1/indicators/",
        json={
            "type": "pm25",
            "value": 20,
            "unit": "µg/m3",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "zone_id": zone["id"],
            "source_id": source["id"],
        },
        headers=headers,
    )
    return zone["id"]


def test_stats_endpoints(client: TestClient, admin_user):
    token = authenticate(client, admin_user["email"], admin_user["password"])
    headers = {"Authorization": f"Bearer {token}"}
    zone_id = seed_indicator(client, headers)

    avg_resp = client.get(f"/api/v1/stats/air/averages?zone_id={zone_id}", headers=headers)
    assert avg_resp.status_code == 200
    assert avg_resp.json()["zone_id"] == zone_id

    trend_resp = client.get(
        f"/api/v1/stats/trend?zone_id={zone_id}&indicator_type=pm25", headers=headers
    )
    assert trend_resp.status_code == 200
    assert trend_resp.json()["indicator_type"] == "pm25"
