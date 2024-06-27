from sqlmodel import SQLModel, Field, Relationship
from typing import List, Literal, Optional
from datetime import timezone, datetime
from .base import BaseIdModel
from sqlalchemy import func
# import datetime

class OrderItemBase(SQLModel):
    product_id: int = Field(foreign_key="product.id")
    product_item_id: int = Field(foreign_key="productitem.id")
    product_size_id: int = Field(foreign_key="productsize.id")
    quantity: int


class OrderBase(SQLModel):
    order_address: str
    phone_number: str 



class OrderModel(OrderBase):
    items: List[OrderItemBase]


class Order(BaseIdModel, OrderBase, table=True):
    total_price: float
    order_status: str = Field(default="pending")
    order_date: datetime | None = Field(default=datetime.now(timezone.utc))
    user_id: int = Field(foreign_key="users.id")
    order_items: List["OrderItem"] = Relationship(back_populates="order")


class OrderItem(BaseIdModel, OrderItemBase, table=True):
    order_id: int = Field(foreign_key="order.id")
    order: Optional["Order"] = Relationship(back_populates="order_items")

class OrderUpdateStatus(SQLModel):
    order_id: int
    status: str