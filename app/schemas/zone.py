from typing import Optional

from pydantic import BaseModel, Field


class ZoneBase(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    postal_code: Optional[str] = Field(default=None, max_length=20)
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)
    description: Optional[str] = Field(default=None, max_length=1024)


class ZoneCreate(ZoneBase):
    pass


class ZoneUpdate(BaseModel):
    name: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None


class ZonePublic(ZoneBase):
    id: int

    class Config:
        from_attributes = True
