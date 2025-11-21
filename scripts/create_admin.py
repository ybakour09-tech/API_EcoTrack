import click
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.user import User


@click.command()
@click.option("--email", default=settings.first_superuser_email, prompt="Email")
@click.option("--password", default=settings.first_superuser_password, prompt=True, hide_input=True, confirmation_prompt=True)
@click.option("--full-name", default="EcoTrack Admin", prompt="Nom complet")
def create_admin(email: str, password: str, full_name: str):
    db: Session = SessionLocal()
    try:
        if db.query(User).filter(User.email == email).first():
            click.echo("Un utilisateur existe déjà avec cet email.")
            return
        admin = User(
            email=email,
            full_name=full_name,
            hashed_password=get_password_hash(password),
            role="admin",
        )
        db.add(admin)
        db.commit()
        click.echo(f"Administrateur {email} créé.")
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()