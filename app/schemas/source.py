from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class SourceBase(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    url: Optional[HttpUrl] = None
    description: Optional[str] = Field(default=None, max_length=1024)


class SourceCreate(SourceBase):
    pass


class SourceUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[HttpUrl] = None
    description: Optional[str] = None


class SourcePublic(SourceBase):
    id: int

    class Config:
        from_attributes = True
