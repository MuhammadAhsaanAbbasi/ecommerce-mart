from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from .base import BaseIdModel


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

class CartUpdateItem(SQLModel):
    cart_item_id: str
    quantity: int
