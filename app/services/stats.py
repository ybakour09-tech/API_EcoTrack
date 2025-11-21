from __future__ import annotations

from datetime import datetime
from typing import Literal

from sqlalchemy import extract, func, select
from sqlalchemy.orm import Session

from app.models.indicator import Indicator


def get_average_air_quality(
    db: Session,
    *,
    zone_id: int | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    indicator_type: str = "pm25",
):
    stmt = select(
        func.avg(Indicator.value).label("average"),
        func.min(Indicator.timestamp).label("start"),
        func.max(Indicator.timestamp).label("end"),
    ).where(Indicator.type == indicator_type)

    if zone_id:
        stmt = stmt.where(Indicator.zone_id == zone_id)
    if date_from:
        stmt = stmt.where(Indicator.timestamp >= date_from)
    if date_to:
        stmt = stmt.where(Indicator.timestamp <= date_to)

    result = db.execute(stmt).mappings().one()
    return {
        "type": indicator_type,
        "zone_id": zone_id,
        "average": result["average"],
        "start": result["start"],
        "end": result["end"],
    }


def get_trend(
    db: Session,
    *,
    zone_id: int,
    indicator_type: str,
    period: Literal["daily", "weekly", "monthly"] = "monthly",
):
    if period == "daily":
        grouping = func.date(Indicator.timestamp)
    elif period == "weekly":
        grouping = func.strftime("%Y-%W", Indicator.timestamp)
    else:
        grouping = func.strftime("%Y-%m", Indicator.timestamp)

    stmt = (
        select(grouping.label("bucket"), func.avg(Indicator.value).label("value"))
        .where(Indicator.zone_id == zone_id, Indicator.type == indicator_type)
        .group_by("bucket")
        .order_by("bucket")
    )

    rows = db.execute(stmt).mappings().all()
    return {"period": period, "indicator_type": indicator_type, "series": rows}
