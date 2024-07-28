from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from .base import BaseIdModel
from ..model.product import ProductDetails


class CartItemModel(SQLModel):
    quantity: int = Field(default=1)
    product_item_id: str = Field(default=None, foreign_key="productitem.id")
    product_size_id: str = Field(default=None, foreign_key="productsize.id")

class Cart(BaseIdModel, table=True):
    user_id: int = Field(foreign_key="users.id")
    cart_items: List["CartItem"] = Relationship(back_populates="cart")

class CartItem(CartItemModel, BaseIdModel, table=True):
    cart_id: str = Field(foreign_key="cart.id")
    cart: Optional["Cart"] = Relationship(back_populates="cart_items")


class CartToken(SQLModel):
    quantity: int = Field(default=1)
    product_id: str = Field(default=None, foreign_key="product.id")
    product_item_id: str = Field(default=None, foreign_key="productitem.id")
    product_size_id: str = Field(default=None, foreign_key="productsize.id")

class CartItemDetail(SQLModel):
    cart_item_id: str
    quantity: int
    cart_item_total_price: float
    product_details: ProductDetails

class CartDetails(SQLModel):
    cart_items: List[CartItemDetail]
    total_price: float