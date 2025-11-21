from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    url: Mapped[str | None] = mapped_column(String(512))
    description: Mapped[str | None] = mapped_column(String(1024))

    indicators = relationship("Indicator", back_populates="source", cascade="all,delete")
