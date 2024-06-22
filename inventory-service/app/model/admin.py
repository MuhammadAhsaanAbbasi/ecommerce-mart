from sqlmodel import SQLModel, Field,Relationship
from typing import Optional
from pydantic import BaseModel, EmailStr
from .base import BaseIdModel
import uuid

class UserBase(SQLModel):
    kid: Optional[str] = Field(default=uuid.uuid4().hex)
    username: str = Field(index=True)
    email: str = Field(index=True)
    hashed_password: Optional[str] = Field(default=None, index=True)
    imageUrl: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    otp: Optional[str] = Field(default=None, index=True)

# Admin Model
class Admin(UserBase, BaseIdModel, table=True):
    role: str = Field(default="admin")

class Token(SQLModel):
    access_token: str
    token_type: str
    access_expires_in: int
    refresh_token: str
    refresh_token_expires_in: int

class TokenData(BaseModel):
    username: str | None = None
    email: str | None = None