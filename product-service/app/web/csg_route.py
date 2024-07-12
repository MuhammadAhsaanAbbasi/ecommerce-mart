from fastapi import APIRouter, Depends, UploadFile, File
from typing import Annotated
from sqlmodel import Session
from ..utils.utils import create_categories, get_categories, create_genders, get_all_genders, create_sizes, get_sizies
from ..core.db import DB_SESSION
from ..model.category_model import Category, Size, Gender, CategoryBase

csg_router = APIRouter(prefix="/api/v1/csg")

# Category Routes
@csg_router.post("/create_category") 
async def create_category(
                        category_input: CategoryBase, 
                        session: DB_SESSION,
                        category_image: UploadFile = File(...),
                        ):
    category = await create_categories(category_input,session, category_image)
    return {"message": "Create Product Category Successfully!", "data" : category}

@csg_router.get("/get_category")
async def get_category(session: DB_SESSION):
    category = await get_categories(session)
    return category


# Size Routes
@csg_router.post("/create_size")
async def create_size(size_input: Size, session: DB_SESSION):
    size = await create_sizes(size_input,session)
    return {"message": "Create Product Size Successfully!", "data" : size}

@csg_router.get("/get_sizes")
async def get_sizes(session: DB_SESSION):
    size = await get_sizies(session)
    return size


# Gender Routes
@csg_router.post("/create_gender")
async def create_gender(gender_input: Gender, session: DB_SESSION):
    gender = await create_genders(gender_input,session)
    return {"message": "Create Product Genders Successfully!", "data" : gender}

@csg_router.get("/get_genders")
async def get_genders(session: DB_SESSION):
    genders = await get_all_genders(session)
    return genders