from sqlmodel import SQLModel, Field,Relationship
from typing import Optional
from pydantic import BaseModel, EmailStr
from .base import BaseIdModel

class EmailUser(BaseModel):
    username: str
    email: str
    imageUrl: str
    is_active: bool
    is_verified: bool
    role: str

