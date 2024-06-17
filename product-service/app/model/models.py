from sqlmodel import SQLModel, Field,Relationship
from typing import Optional, List, Literal
import datetime
from pydantic import BaseModel, EmailStr
from .base import BaseIdModel
# import requests

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
    price: str = Field(ge=0)
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

class SizeModel(SQLModel):
    """
    Model for representing size details in forms.

    Attributes:
        size (str | int): Size of the product item.
        price (int): Price of the product item.
        stock (int): Stock level of the product item.
    """
    size: str | int
    price: int = Field(ge=0)
    stock: int

class ProductItemBase(SQLModel):
    """
    Base model for ProductItem, used for shared attributes.

    Attributes:
        color (str): Color of the product item.
    """
    color: str

class ProductItemFormModel(ProductItemBase):
    """
    Model for representing product item details in forms.

    Attributes:
    color (str): Color of the product item.
    image_url (str): URL of the product item image.
    sizes (list[SizeModel]): List of size details.
    """
    image_url: str
    sizes: List[SizeModel]

class ProductFormModel(ProductBase):
    """
    Model for representing product details in forms.

    Attributes:
    product_item (list[ProductItemFormModel]): List of product item details.
    """
    product_item: List[ProductItemFormModel]