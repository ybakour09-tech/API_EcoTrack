from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: str = Field(default="user", pattern="^(user|admin)$")
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)
    role: str = "user"


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = Field(default=None, pattern="^(user|admin)$")
    is_active: Optional[bool] = None
    password: Optional[str] = Field(default=None, min_length=8, max_length=128)


class UserPublic(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
