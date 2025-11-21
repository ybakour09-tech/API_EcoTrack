from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Indicator(Base):
    __tablename__ = "indicators"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    type: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(25), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    zone_id: Mapped[int] = mapped_column(ForeignKey("zones.id", ondelete="CASCADE"), nullable=False)
    source_id: Mapped[int] = mapped_column(
        ForeignKey("sources.id", ondelete="SET NULL"), nullable=True
    )
    payload: Mapped[dict | None] = mapped_column("metadata", JSON, default=dict)

    zone = relationship("Zone", back_populates="indicators")
    source = relationship("Source", back_populates="indicators")
