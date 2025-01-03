from sqlmodel import SQLModel, Field,Relationship
from typing import Optional, List, Literal, Union
import datetime
from pydantic import BaseModel, EmailStr
from .base import BaseIdModel
from uuid import UUID
import uuid

class Color(BaseIdModel, table=True):
    color_name: str
    color_value: str

# Product Base Model
class ProductBase(BaseIdModel):
    """
    Base model for Product, used for shared attributes.

    Attributes:
        product_name (str): Name of the product.
        description (str): Description of the product.
    """
    product_name: str = Field(index=True)
    product_desc: Optional[str] = Field(default=None)
    featured: bool = Field(default=False)
    category_id: str = Field(foreign_key="category.id")

class Product(ProductBase, table=True):
    """
    Fields:
    product_name, product_desc, category_id, gender_id (required): inherited from ProductBase
    """
    product_item: List["ProductItem"] = Relationship(back_populates="product")

class ProductItem(BaseIdModel, table=True):
    image_url: str
    color: str = Field(foreign_key="color.id")
    product_id: str = Field(foreign_key="product.id")
    product: Optional["Product"] = Relationship(back_populates="product_item")
    sizes: List["ProductSize"] = Relationship(back_populates="product_item")

class ProductSize(BaseIdModel, table=True):
    price: int = Field(ge=0)
    size: str = Field(foreign_key="size.id")
    stock: "Stock" = Relationship(back_populates="product_size")
    product_item_id: str = Field(foreign_key="productitem.id")
    product_item: Optional["ProductItem"] = Relationship(back_populates="sizes")

class Stock(BaseIdModel, table=True):
    product_size_id: str = Field(foreign_key="productsize.id")
    stock: int = 0
    product_size: Optional[ProductSize] = Relationship(back_populates="stock")
    
    @property
    def stock_level(self) -> Literal["High", "Medium", "Low"]:
        if self.stock > 100:
            return "High"
        elif self.stock > 50:
            return "Medium"
        else:
            return "Low"

class ReviewModel(SQLModel):
    rating: int
    review: str
    product_id: str

class Review(BaseIdModel, table=True):
    rating: int = Field(ge=1, le=5)
    review: str
    product_id: str = Field(foreign_key="product.id")
    user_id: int = Field(foreign_key="users.id")

class ProductReviewsDetails(SQLModel):
    review_id: str
    rating: int
    review: str
    username: str
    email: str
    imageUrl: Optional[str] = Field(default=None)  # Make imageUrl optional

class UserReviewsDetails(SQLModel):
    review_id: str
    rating: int
    review: str
    product_id: str
    product_name: str


class SizeModel(SQLModel):
    size: str
    price: int
    stock: int

class ProductItemFormModel(SQLModel):
    color: str
    image_url: Optional[str] = Field(default=None)
    sizes: List[SizeModel]

class ProductBaseForm(SQLModel):
    product_name: str
    product_desc: Optional[str]
    featured: bool
    category_id: str

class ProductFormModel(ProductBaseForm):
    product_item: List[ProductItemFormModel]

class SizeModelDetails(SQLModel):
    """
    Model for representing size details in forms.

    Attributes:
        size (str | int): Size of the product item.
        price (int): Price of the product item.
        stock (int): Stock level of the product item.
    """
    product_size_id: Optional[str]
    size: Union[int , str]
    price: int
    stock: int

class ProductItemDetails(SQLModel):
    product_item_id: Optional[str]
    color_name: str
    color_value: str
    color: str
    image_url: Optional[str] = Field(default=None)
    sizes: List[SizeModelDetails]

class ProductDetails(ProductBaseForm):
    product_id: Optional[str]
    product_item: List[ProductItemDetails]