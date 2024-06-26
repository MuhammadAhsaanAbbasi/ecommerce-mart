from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from .base import BaseIdModel

class CartBase(SQLModel):
    user_id: int = Field(foreign_key="users.id")

class CartItemBase(SQLModel):
    quantity: int = Field(default=1)
    product_item_id: int = Field(default=None, foreign_key="productitem.id")
    product_size_id: int = Field(default=None, foreign_key="productsize.id")

class CartModel(CartBase, CartItemBase):
    pass

class Cart(CartBase, BaseIdModel, table=True):
    cart_items: list["CartItem"] = Relationship(back_populates="cart")

class CartItem(CartItemBase, BaseIdModel, table=True):
    cart_id: int = Field(foreign_key="cart.id")
    cart: Optional["Cart"] = Relationship(back_populates="cart_items")

class CartUpdateItem(SQLModel):
    cart_item_id: int
    quantity: int
