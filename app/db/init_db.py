from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User


def init_db(db: Session):
    admin = db.query(User).filter(User.email == settings.first_superuser_email).first()
    if not admin:
        admin = User(
            email=settings.first_superuser_email,
            full_name="EcoTrack Admin",
            hashed_password=get_password_hash(settings.first_superuser_password),
            role="admin",
            is_active=True,
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
