from sqlmodel import SQLModel, Field,Relationship
from typing import Optional, Union, List
from pydantic import BaseModel, EmailStr
from .base import BaseIdModel

class EmailUser(BaseModel):
    username: str
    email: str
    imageUrl: str
    is_active: bool
    is_verified: bool
    role: str

class SizeModel(SQLModel):
    """
    Model for representing size details in forms.

    Attributes:
        size (str | int): Size of the product item.
        price (int): Price of the product item.
        stock (int): Stock level of the product item.
    """
    size: int
    price: float
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
    category_id: Union[int , str]
    gender_id: Union[int , str]


class ProductFormModel(ProductBaseForm):
    """
    Model for representing product details in forms.

    Attributes:
    product_item (list[ProductItemFormModel]): List of product item details.
    """
    product_item: List[ProductItemFormModel]