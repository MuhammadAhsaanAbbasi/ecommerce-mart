from ..model.category_model import Category, Size, Gender
from typing import List
from sqlmodel import SQLModel, select, Session
from ..core.db import DB_SESSION
from fastapi import Depends

# Create Categories
async def create_categories(category_input: Category, session: DB_SESSION):
    category = Category(**category_input.model_dump())
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

# Get Categories
async def get_categories(session: DB_SESSION):
    categories = session.exec(select(Category)).all()
    return {"data" : categories}

# Create Size
async def create_sizes(size_input: Size, session: DB_SESSION):
    size = Size(**size_input.model_dump())
    session.add(size)
    session.commit()
    session.refresh(size)
    return size

# Get Sizes
async def get_sizies(session: DB_SESSION):
    sizes = session.exec(select(Size)).all()
    return {"data" : sizes}

# Create Genders
async def create_genders(gender_input: Gender, session: DB_SESSION):
    gender = Gender(**gender_input.model_dump())
    session.add(gender)
    session.commit()
    session.refresh(gender)
    return gender

# Get Genders
async def get_all_genders(session: DB_SESSION):
    genders = session.exec(select(Gender)).all()
    return {"data" : genders}

# Search Algorithm By Category
async def search_algorithm_by_category(input: str, session: DB_SESSION):
    """Search for categories that start with the given input."""
    categories = session.exec(select(Category).where(Category.category_name.startswith(input))).all()
    return categories