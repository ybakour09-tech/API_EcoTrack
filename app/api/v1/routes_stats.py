from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_active_user
from app.db.session import get_db
from app.services.stats import get_average_air_quality, get_trend

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/air/averages")
def air_averages(
    *,
    db: Session = Depends(get_db),
    zone_id: int | None = Query(default=None),
    indicator_type: str = Query(default="pm25"),
    date_from: datetime | None = Query(default=None),
    date_to: datetime | None = Query(default=None),
    _: object = Depends(get_current_active_user),
):
    return get_average_air_quality(
        db,
        zone_id=zone_id,
        indicator_type=indicator_type,
        date_from=date_from,
        date_to=date_to,
    )


@router.get("/trend")
def trend(
    *,
    db: Session = Depends(get_db),
    zone_id: int,
    indicator_type: str,
    period: str = Query("monthly", enum=["daily", "weekly", "monthly"]),
    _: object = Depends(get_current_active_user),
):
    return get_trend(db, zone_id=zone_id, indicator_type=indicator_type, period=period)
