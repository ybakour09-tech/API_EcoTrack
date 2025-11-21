from __future__ import annotations

from functools import lru_cache
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import Settings, get_settings


@lru_cache
def _get_engine():
    settings = get_settings()
    connect_args = {}

    if settings.database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False

    return create_engine(
        settings.database_url,
        future=True,
        echo=settings.sqlalchemy_echo,
        connect_args=connect_args,
    )


engine = _get_engine()

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    future=True,
)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
