from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin, get_current_active_user
from app.db.session import get_db
from app.models.zone import Zone
from app.schemas.zone import ZoneCreate, ZonePublic, ZoneUpdate

router = APIRouter(prefix="/zones", tags=["zones"])


@router.get("/", response_model=list[ZonePublic])
def list_zones(
    *,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    _: object = Depends(get_current_active_user),
):
    return db.query(Zone).offset(skip).limit(limit).all()


@router.post("/", response_model=ZonePublic, status_code=status.HTTP_201_CREATED)
def create_zone(
    *,
    db: Session = Depends(get_db),
    payload: ZoneCreate,
    _: object = Depends(get_current_admin),
):
    zone = Zone(**payload.model_dump())
    db.add(zone)
    db.commit()
    db.refresh(zone)
    return zone


@router.patch("/{zone_id}", response_model=ZonePublic)
def update_zone(
    *,
    db: Session = Depends(get_db),
    zone_id: int,
    payload: ZoneUpdate,
    _: object = Depends(get_current_admin),
):
    zone = db.get(Zone, zone_id)
    if not zone:
        raise HTTPException(status_code=404, detail="Zone introuvable")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(zone, field, value)
    db.commit()
    db.refresh(zone)
    return zone


@router.delete("/{zone_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_zone(
    *,
    db: Session = Depends(get_db),
    zone_id: int,
    _: object = Depends(get_current_admin),
):
    zone = db.get(Zone, zone_id)
    if not zone:
        raise HTTPException(status_code=404, detail="Zone introuvable")
    db.delete(zone)
    db.commit()
    return None
