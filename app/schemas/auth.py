from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None


class LoginResponse(BaseModel):
    token: Token
    user_id: int
    email: str  # Changed from EmailStr to avoid re-validation issues
    role: str
    expires_at: datetime
