from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from enum import Enum
from datetime import timezone, datetime, timedelta
from .base import BaseIdModel
import uuid

class OrderItemBase(SQLModel):
    product_id: str = Field(foreign_key="product.id")
    product_item_id: str = Field(foreign_key="productitem.id")
    product_size_id: str = Field(foreign_key="productsize.id")
    quantity: int

class OrderPayment(str, Enum):
    cash_on_delivery = "Cash On Delivery" 
    online_payment = "Online Payment"

class OrderDelivery(SQLModel):
    email: str
    country: str
    city: str
    postal_code: str
    address: str
    phone_number: str

class OrderBase(OrderDelivery):
    total_price: float
    order_payment: OrderPayment = Field(default="Cash On Delivery")

class OrderModel(OrderBase):
    items: List[OrderItemBase]

class OrderStatus(str, Enum):
    processing = "processing"
    shipping = "shipping"
    delivered = "delivered"
    cancelled = "cancelled"


def calculate_delivery_date():
    return datetime.now(timezone.utc) + timedelta(days=7)

class Order(BaseIdModel, OrderBase, table=True):
    tracking_id: Optional[str] = Field(default=uuid.uuid4().hex)
    order_status: Optional[OrderStatus] = Field(default="processing")
    delivery_date: datetime | None = Field(default_factory=calculate_delivery_date)
    order_date: datetime | None = Field(default=datetime.now(timezone.utc))
    user_id: int = Field(foreign_key="users.id")
    order_items: List["OrderItem"] = Relationship(back_populates="order")


class OrderItem(BaseIdModel, OrderItemBase, table=True):
    order_id: str = Field(foreign_key="order.id") 
    order: Optional["Order"] = Relationship(back_populates="order_items")

class OrderItemDetails(SQLModel):
    product_name: str
    product_image_url: str
    product_color: str
    product_size: str
    quantity: int
    price: int


class OrderDetails(OrderBase):
    order_id: str
    delivery_charges: int = 1000
    order_items: List[OrderItemDetails]