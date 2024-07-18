from sqlmodel import SQLModel, Field,Relationship
from typing import Optional
from datetime import datetime
from pydantic import EmailStr
from .base import BaseIdModel
from .authentication import Users
import uuid

class TransactionModel(SQLModel):
    stripeId: str
    amount: str
    order_id: str

class Transaction(BaseIdModel, TransactionModel, table=True):
    transaction_id: Optional[str] = Field(default=uuid.uuid4().hex)
    user_id: int = Field(foreign_key="users.id")


class TransactionDetail(SQLModel):
    transaction_id: str
    stripeId: str
    amount: str
    order_id: str
    user_id: int
    username: str
    email: str
    imageUrl: str
    order_address: str
    phone_number: str
    total_price: float
    order_status: str
    delivery_date: datetime
    order_date: datetime