import click

from app.db.session import SessionLocal
from app.services.ingestion import fetch_openaq, save_measurements


@click.command()
@click.option("--limit", default=5, show_default=True, help="Nombre de points à importer (par capteur ou par station)")
@click.option("--city", default=None, help="Filtrer par ville (nom ou partie du nom renvoyé par l'API OpenAQ)")
@click.option("--country", default=None, help="Code pays ISO alpha-2 (ex: FR, US)")
@click.option("--location-id", type=int, default=None, help="Identifiant précis d'une localisation OpenAQ")
def ingest(limit: int, city: str | None, country: str | None, location_id: int | None):
    """
    Script d'ingestion OpenAQ.

    - Avec --location-id : historique par capteur pour une localisation donnée
    - Avec --city / --country : snapshot des dernières valeurs par station
    """
    if not any([city, country, location_id]):
        raise click.BadParameter(
            "Merci de préciser au moins un filtre (--city, --country ou --location-id) "
            "afin d'éviter l'erreur 404 de l'API OpenAQ."
        )

    measurements = fetch_openaq(
        limit=limit,
        city=city,
        country=country,
        location_id=location_id,
    )
    db = SessionLocal()
    try:
        created = save_measurements(db, measurements)
        click.echo(f"{created} indicateurs créés.")
    finally:
        db.close()


if __name__ == "__main__":
    ingest()
