from __future__ import annotations

import secrets
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = "EcoTrack API"
    environment: str = Field(default="development", alias="ENVIRONMENT")
    api_v1_prefix: str = "/api/v1"

    # Security
    secret_key: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Database
    database_url: str = Field(default="sqlite:///./ecotrack.db", alias="DATABASE_URL")
    sqlalchemy_echo: bool = False

    # External APIs
    openaq_api_key: str | None = Field(default=None, alias="OPENAQ_API_KEY")

    # Default admin bootstrap
    first_superuser_email: str = "admin@ecotrack.local"
    first_superuser_password: str = "ChangeMe123!"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
