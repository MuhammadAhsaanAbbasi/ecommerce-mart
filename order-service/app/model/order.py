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
    order_address: str = Field(max_length=60)
    phone_number: str = Field(max_length=15)


class OrderModel(OrderBase):
    items: List[OrderItemBase]


class Order(OrderBase, table=True):
    total_price: float
    order_status: str = Field(default="pending")
    order_date: Optional[datetime.datetime] = Field(
        sa_column_kwargs={"server_default": "CURRENT_TIMESTAMP"},
        default_factory=datetime.datetime.now,
    )
    user_id: int = Field(foreign_key="users.id")
    order_items: list["OrderItem"] = Relationship(back_populates="order")


class OrderItem(OrderItemBase, BaseIdModel, table=True):
    order_id: int = Field(foreign_key="order.order_id")
    order: Optional[Order] = Relationship(back_populates="items")

class OrderUpdateStatus(SQLModel):
    order_id: int
    status: str

# Product Base Model
class ProductBase(SQLModel):
    """
    Base model for Product, used for shared attributes.

    Attributes:
        product_name (str): Name of the product.
        description (str): Description of the product.
    """
    product_name: str = Field(index=True)
    product_desc: Optional[str] = Field(default=None)
    category_id: int = Field(foreign_key="category.id")
    gender_id: int = Field(foreign_key="gender.id")

class Product(ProductBase, BaseIdModel, table=True):
    """
    Fields:
    product_name, product_desc, category_id, gender_id (required): inherited from ProductBase
    """
    product_item: List["ProductItem"] = Relationship(back_populates="product")

class ProductItem(BaseIdModel, table=True):
    """
    Fields:
    product_name, product_desc, category_id, gender_id (required): inherited from ProductBase]
    """
    color: str
    image_url: str
    product_id: int = Field(foreign_key="product.id")
    product: Optional["Product"] = Relationship(back_populates="product_item")
    sizes: List["ProductSize"] = Relationship(back_populates="product_item")

class ProductSize(BaseIdModel, table=True):
    """
    Fields:
    product_name, product_desc, category_id, gender_id (required): inherited from ProductBase]
    """
    size: int = Field(foreign_key="size.id")
    price: int = Field(ge=0)
    stock: "Stock" = Relationship(back_populates="product_size")
    product_item_id: int = Field(foreign_key="productitem.id")
    product_item: Optional["ProductItem"] = Relationship(back_populates="sizes")

class Stock(BaseIdModel, table=True):
    """
    Fields:
    product_name, product_desc, category_id, gender_id (required): inherited from ProductBase]
    """
    product_size_id: Optional[int] = Field(
        # Foreign key linking to ProductSize
        default=None, foreign_key="productsize.id")
    stock: int = 0  # Stock level
    product_size: Optional[ProductSize] = Relationship(
        back_populates="stock")  # One-to-one relationship with ProductSize
    
    @property
    def stock_level(self) -> Literal["High", "Medium", "Low"]:
        if self.stock > 100:
            return "High"
        elif self.stock > 50:
            return "Medium"
        else:
            return "Low"