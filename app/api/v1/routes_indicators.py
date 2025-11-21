from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin, get_current_active_user
from app.db.session import get_db
from app.models.indicator import Indicator
from app.schemas.indicator import (
    IndicatorCreate,
    IndicatorListResponse,
    IndicatorPublic,
    IndicatorUpdate,
)
from app.services.indicators import count_indicators, list_indicators

router = APIRouter(prefix="/indicators", tags=["indicators"])


@router.get("/", response_model=IndicatorListResponse)
def read_indicators(
    *,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    indicator_type: str | None = Query(default=None),
    zone_id: int | None = Query(default=None),
    source_id: int | None = Query(default=None),
    date_from: datetime | None = Query(default=None),
    date_to: datetime | None = Query(default=None),
    _: object = Depends(get_current_active_user),
):
    items = list_indicators(
        db,
        skip=skip,
        limit=limit,
        indicator_type=indicator_type,
        zone_id=zone_id,
        source_id=source_id,
        date_from=date_from,
        date_to=date_to,
    )
    total = count_indicators(
        db,
        indicator_type=indicator_type,
        zone_id=zone_id,
        source_id=source_id,
        date_from=date_from,
        date_to=date_to,
    )
    return IndicatorListResponse(total=total, items=items)


@router.post("/", response_model=IndicatorPublic, status_code=status.HTTP_201_CREATED)
def create_indicator(
    *,
    db: Session = Depends(get_db),
    payload: IndicatorCreate,
    _: object = Depends(get_current_admin),
):
    data = payload.model_dump()
    metadata = data.pop("metadata", None)
    indicator = Indicator(**data)
    if metadata is not None:
        indicator.payload = metadata
    db.add(indicator)
    db.commit()
    db.refresh(indicator)
    return indicator


@router.get("/{indicator_id}", response_model=IndicatorPublic)
def get_indicator(
    *,
    db: Session = Depends(get_db),
    indicator_id: int,
    _: object = Depends(get_current_active_user),
):
    indicator = db.get(Indicator, indicator_id)
    if not indicator:
        raise HTTPException(status_code=404, detail="Indicateur introuvable")
    return indicator


@router.patch("/{indicator_id}", response_model=IndicatorPublic)
def update_indicator(
    *,
    db: Session = Depends(get_db),
    indicator_id: int,
    payload: IndicatorUpdate,
    _: object = Depends(get_current_admin),
):
    indicator = db.get(Indicator, indicator_id)
    if not indicator:
        raise HTTPException(status_code=404, detail="Indicateur introuvable")
    data = payload.model_dump(exclude_unset=True)
    metadata = data.pop("metadata", None)
    for field, value in data.items():
        setattr(indicator, field, value)
    if metadata is not None:
        indicator.payload = metadata
    db.commit()
    db.refresh(indicator)
    return indicator


@router.delete("/{indicator_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_indicator(
    *,
    db: Session = Depends(get_db),
    indicator_id: int,
    _: object = Depends(get_current_admin),
):
    indicator = db.get(Indicator, indicator_id)
    if not indicator:
        raise HTTPException(status_code=404, detail="Indicateur introuvable")
    db.delete(indicator)
    db.commit()
    return None
