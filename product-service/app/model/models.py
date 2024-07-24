from sqlmodel import SQLModel, Field,Relationship
from typing import Optional, List, Literal, Union
import datetime
from pydantic import BaseModel, EmailStr
from .base import BaseIdModel
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
    category_id: uuid.UUID = Field(foreign_key="category.id")

class Product(ProductBase, table=True):
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
    image_url: str
    color: uuid.UUID = Field(foreign_key="color.id")
    product_id: uuid.UUID = Field(foreign_key="product.id")
    product: Optional["Product"] = Relationship(back_populates="product_item")
    sizes: List["ProductSize"] = Relationship(back_populates="product_item")

class ProductSize(BaseIdModel, table=True):
    """
    Fields:
    product_name, product_desc, category_id, gender_id (required): inherited from ProductBase]
    """
    price: int = Field(ge=0)
    size: uuid.UUID = Field(foreign_key="size.id")
    stock: "Stock" = Relationship(back_populates="product_size")
    product_item_id: uuid.UUID = Field(foreign_key="productitem.id")
    product_item: Optional["ProductItem"] = Relationship(back_populates="sizes")

class Stock(BaseIdModel, table=True):
    """
    Fields:
    product_name, product_desc, category_id , gender_id (required): inherited from ProductBase]
    """
    product_size_id: Optional[uuid.UUID] = Field(
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
    size: int
    price: int
    stock: int

class ProductItemFormModel(SQLModel):
    """
    Model for representing product item details in forms.

    Attributes:
    color (str): Color of the product item.
    image_url (str): URL of the product item image.
    sizes (list[SizeModel]): List of size details.
    """
    color: str
    image_url: Optional[str] = Field(default=None)
    sizes: List[SizeModel]

class ProductBaseForm(SQLModel):
    """
    Base model for Product, used for shared attributes.

    Attributes:
        product_name (str): Name of the product.
        description (str): Description of the product. 
    """
    product_name: str
    product_desc: Optional[str]
    featured: bool
    category_id: Union[int , str]


class ProductFormModel(ProductBaseForm):
    """
    Model for representing product details in forms.

    Attributes:
    product_item (list[ProductItemFormModel]): List of product item details.
    """
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
    """
    Model for representing product item details in forms.

    Attributes:
    color (str): Color of the product item.
    image_url (str): URL of the product item image.
    sizes (list[SizeModel]): List of size details.
    """
    product_item_id: Optional[str]
    color: str
    image_url: Optional[str] = Field(default=None)
    sizes: List[SizeModel]

class ProductDetails(ProductBaseForm):
    """
    Model for representing product details in forms.

    Attributes:
    product_item (list[ProductItemFormModel]): List of product item details.
    """
    product_id: Optional[str]
    product_item: List[ProductItemFormModel]