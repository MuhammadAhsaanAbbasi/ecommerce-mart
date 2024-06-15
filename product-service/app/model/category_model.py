from sqlmodel import SQLModel, Field, Relationship
from .base import BaseIdModel

# Category Class
class Category(BaseIdModel, table=True):
    category_name: str = Field(index=True)
    category_desc: str 

# Gender Class
class Gender(BaseIdModel, table=True):
    gender_name: str = Field(index=True)

# Size Class
class Size(BaseIdModel, table=True):
    """
    Represents a specific size within a size category.

    Attributes:
        size_id (Optional[int]): Primary key for Size.
        size (str | int): Size of the product (e.g., S, M, L, 8, 9).
    """
    size_name: str | int = Field(index=True) # xs, sm, md, lg, xl

