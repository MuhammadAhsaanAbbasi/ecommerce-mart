from sqlmodel import SQLModel, Field, Relationship
from typing import List, Literal, Optional
from datetime import timezone
import datetime
from .authentication import UserBase
from .base import BaseIdModel

class OrderItemBase(SQLModel):
    product_id: int = Field(foreign_key="product.product_id")
    product_item_id: int = Field(foreign_key="productitem.item_id")
    product_size_id: int = Field(foreign_key="productsize.product_size_id")
    quantity: int


class OrderBase(BaseIdModel):
    user_id: int = Field(foreign_key="users.id")
    order_address: str = Field(max_length=60)


class OrderModel(OrderBase):
    items: List[OrderItemBase]


class Order(OrderBase, table=True):
    total_price: float
    advance_price: Optional[float]
    order_status: str = Field(default="pending")
    order_date: Optional[datetime.datetime] = Field(
        sa_column_kwargs={"server_default": "CURRENT_TIMESTAMP"},
        default_factory=datetime.datetime.now,
    )
    order_items: list["OrderItem"] = Relationship(back_populates="order")


class OrderItem(OrderItemBase, BaseIdModel, table=True):
    order_id: int = Field(foreign_key="order.order_id")
    order: Optional[Order] = Relationship(back_populates="items")