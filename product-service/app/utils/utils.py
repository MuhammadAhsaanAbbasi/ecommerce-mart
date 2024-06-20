from ..model.category_model import Category, Size, Gender
from typing import Annotated, Optional, Union
from sqlmodel import SQLModel, select, Session
from ..core.db import get_session
from fastapi import Depends

async def create_categories(category_input: Category, session: Annotated[Session, Depends(get_session)]):
    category = Category(**category_input.model_dump())
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

async def get_categories(session: Annotated[Session, Depends(get_session)]):
    categories = session.exec(select(Category)).all()
    return {"data" : categories}


async def create_sizes(size_input: Size, session: Annotated[Session, Depends(get_session)]):
    size = Size(**size_input.model_dump())
    session.add(size)
    session.commit()
    session.refresh(size)
    return size

async def get_sizies(session: Annotated[Session, Depends(get_session)]):
    sizes = session.exec(select(Size)).all()
    return {"data" : sizes}

async def create_genders(gender_input: Gender, session: Annotated[Session, Depends(get_session)]):
    gender = Gender(**gender_input.model_dump())
    session.add(gender)
    session.commit()
    session.refresh(gender)
    return gender

async def get_all_genders(session: Annotated[Session, Depends(get_session)]):
    genders = session.exec(select(Gender)).all()
    return {"data" : genders}