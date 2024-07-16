from sqlmodel import SQLModel, Field,Relationship
from typing import Optional
import datetime
from pydantic import BaseModel, EmailStr
from .base import BaseIdModel
import uuid

class TransactionModel(SQLModel):
    stripeId: str
    amount: str
    order_id: str

class Transaction(BaseIdModel, TransactionModel, table=True):
    transaction_id: Optional[str] = Field(default=uuid.uuid4().hex)
    user_id: str = Field(foreign_key="user.id")