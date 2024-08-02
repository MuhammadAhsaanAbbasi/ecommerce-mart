from sqlmodel import SQLModel, Field,Relationship
from typing import Optional, Union, List
from pydantic import BaseModel, EmailStr
# from .base import BaseIdModel

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