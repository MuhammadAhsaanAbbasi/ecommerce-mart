from sqlmodel import SQLModel, Field,Relationship
from typing import Optional
import datetime
from .authentication import UserBase
from .base import BaseIdModel


class Order(BaseIdModel, table=True):
    order_date: Optional[datetime.datetime] = Field(
        sa_column_kwargs={"server_default": "CURRENT_TIMESTAMP"},
        default_factory=datetime.datetime.now,
    )
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    user: Optional["User"] = Relationship(back_populates="orders")
    order_items: list["OrderItem"] = Relationship(back_populates="order")
    total_amount: float

class OrderItem(BaseIdModel, table=True):
    product_id: int = Field(default=None, foreign_key="product.id")
    color: str
    size: str
    quantity: int

# User Model
class User(UserBase, BaseIdModel, table=True):
    role: str = Field(default="user")
    orders: list["Order"] = Relationship(back_populates="user")