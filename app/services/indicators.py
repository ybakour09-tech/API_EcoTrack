from __future__ import annotations

from datetime import datetime
from typing import Iterable, Sequence

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from sqlalchemy import func

from app.models.indicator import Indicator

def _apply_filters(
    stmt,
    *,
    indicator_type: str | None,
    zone_id: int | None,
    source_id: int | None,
    date_from: datetime | None,
    date_to: datetime | None,
):
    conditions = []
    if indicator_type:
        conditions.append(Indicator.type == indicator_type)
    if zone_id:
        conditions.append(Indicator.zone_id == zone_id)
    if source_id:
        conditions.append(Indicator.source_id == source_id)
    if date_from:
        conditions.append(Indicator.timestamp >= date_from)
    if date_to:
        conditions.append(Indicator.timestamp <= date_to)
    if conditions:
        stmt = stmt.where(and_(*conditions))
    return stmt


def list_indicators(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 50,
    indicator_type: str | None = None,
    zone_id: int | None = None,
    source_id: int | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> Sequence[Indicator]:
    stmt = select(Indicator).order_by(Indicator.timestamp.desc())
    stmt = _apply_filters(
        stmt,
        indicator_type=indicator_type,
        zone_id=zone_id,
        source_id=source_id,
        date_from=date_from,
        date_to=date_to,
    )
    stmt = stmt.offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def count_indicators(
    db: Session,
    *,
    indicator_type: str | None = None,
    zone_id: int | None = None,
    source_id: int | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> int:
    stmt = select(func.count(Indicator.id))
    stmt = _apply_filters(
        stmt,
        indicator_type=indicator_type,
        zone_id=zone_id,
        source_id=source_id,
        date_from=date_from,
        date_to=date_to,
    )
    return db.scalar(stmt) or 0
