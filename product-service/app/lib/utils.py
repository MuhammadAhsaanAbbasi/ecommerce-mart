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

