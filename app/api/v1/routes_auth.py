from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LoginResponse, Token
from app.schemas.user import UserCreate, UserPublic

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Un utilisateur existe déjà avec cet email")

    db_user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
        role="user",
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login", response_model=LoginResponse)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Email ou mot de passe invalide")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Compte désactivé")

    expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    token = create_access_token(user.id, expires_delta)
    return LoginResponse(
        token=Token(access_token=token),
        user_id=user.id,
        email=user.email,
        role=user.role,
        expires_at=datetime.now(timezone.utc) + expires_delta,
    )
