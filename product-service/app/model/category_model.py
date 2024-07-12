from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, Union
from .base import BaseIdModel

class CategoryBase(BaseIdModel):
    category_name: str = Field(index=True)
    category_desc: str = Field(index=True)

# Category Class
class Category(CategoryBase, table=True):
    category_image: Optional[str]  


# Gender Class
class Gender(BaseIdModel, table=True):
    gender_name: str = Field(index=True)


class Size(BaseIdModel, table=True):
    """
    Represents a specific size within a size category.

    Attributes:
        size_id (Optional[int]): Primary key for Size.
        size (str): Size of the product (e.g., S, M, L, 8, 9).
    """
    size: Optional[str] = Field(index=True)  # xs, sm, md, lg, xl or numeric sizes as strings

    # You can add custom validation logic here if needed.
    @staticmethod
    def validate_size(value: str) -> str:
        if not value.isnumeric() and value not in {"xs", "sm", "md", "lg", "xl"}:
            raise ValueError(f"Invalid size: {value}")
        return value