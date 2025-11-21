from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin, get_current_active_user
from app.db.session import get_db
from app.models.source import Source
from app.schemas.source import SourceCreate, SourcePublic, SourceUpdate

router = APIRouter(prefix="/sources", tags=["sources"])


@router.get("/", response_model=list[SourcePublic])
def list_sources(
    *,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    _: object = Depends(get_current_active_user),
):
    return db.query(Source).offset(skip).limit(limit).all()


@router.post("/", response_model=SourcePublic, status_code=status.HTTP_201_CREATED)
def create_source(
    *,
    db: Session = Depends(get_db),
    payload: SourceCreate,
    _: object = Depends(get_current_admin),
):
    if db.query(Source).filter(Source.name == payload.name).first():
        raise HTTPException(status_code=400, detail="La source existe déjà")
    data = payload.model_dump()
    if data.get("url"):
        data["url"] = str(data["url"])
    source = Source(**data)
    db.add(source)
    db.commit()
    db.refresh(source)
    return source


@router.patch("/{source_id}", response_model=SourcePublic)
def update_source(
    *,
    db: Session = Depends(get_db),
    source_id: int,
    payload: SourceUpdate,
    _: object = Depends(get_current_admin),
):
    source = db.get(Source, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source introuvable")
    data = payload.model_dump(exclude_unset=True)
    if data.get("url"):
        data["url"] = str(data["url"])
    for field, value in data.items():
        setattr(source, field, value)
    db.commit()
    db.refresh(source)
    return source


@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_source(
    *,
    db: Session = Depends(get_db),
    source_id: int,
    _: object = Depends(get_current_admin),
):
    source = db.get(Source, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source introuvable")
    db.delete(source)
    db.commit()
    return None
