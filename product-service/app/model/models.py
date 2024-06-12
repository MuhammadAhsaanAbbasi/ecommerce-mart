from sqlmodel import SQLModel, Field,Relationship
from typing import Optional
import datetime
from pydantic import BaseModel, EmailStr
from .base import BaseIdModel
import requests


class Token(SQLModel):
    access_token: str
    token_type: str
    access_expires_in: int
    refresh_token: str
    refresh_token_expires_in: int

class TokenData(BaseModel):
    username: str | None = None
    email: str | None = None