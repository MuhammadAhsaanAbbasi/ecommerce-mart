from fastapi import APIRouter, Depends
from typing import Annotated
from sqlmodel import Session
from ..core.db import get_session
from ..model.category_model import Category, Size, Gender

csg_router = APIRouter(prefix="/api/v1/csg")

@csg_router.post("/create_category")
async def create_category(category_input: Category, session: Annotated[Session, Depends(get_session)]):
    return {"message": "Create Product Category Successfully!"}

@csg_router.get("/get_category")
async def get_category(session: Annotated[Session, Depends(get_session)]):
    return {"message": "Get Category"}
    
# Additional routes...
