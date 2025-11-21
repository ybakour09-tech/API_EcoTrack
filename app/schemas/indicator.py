from datetime import datetime
from typing import Any, Optional

from pydantic import AliasChoices, BaseModel, Field


class IndicatorBase(BaseModel):
    type: str = Field(min_length=2, max_length=50)
    value: float
    unit: str = Field(min_length=1, max_length=25)
    timestamp: datetime
    zone_id: int
    source_id: Optional[int] = None
    metadata: Optional[dict[str, Any]] = Field(
        default_factory=dict,
        validation_alias=AliasChoices("payload"),
    )


class IndicatorCreate(IndicatorBase):
    pass


class IndicatorUpdate(BaseModel):
    value: Optional[float] = None
    unit: Optional[str] = None
    timestamp: Optional[datetime] = None
    zone_id: Optional[int] = None
    source_id: Optional[int] = None
    metadata: Optional[dict[str, Any]] = None


class IndicatorPublic(IndicatorBase):
    id: int

    class Config:
        from_attributes = True


class IndicatorListResponse(BaseModel):
    total: int
    items: list[IndicatorPublic]
