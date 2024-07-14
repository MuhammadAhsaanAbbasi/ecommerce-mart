from typing import Annotated
from sqlmodel import Session
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from ..utils.utils import create_categories, get_categories, create_genders, get_all_genders, create_sizes, get_sizies, update_categories
from ..model.category_model import Category, Size, Gender, CategoryBaseModel
from ..utils.admin_verify import get_current_active_admin_user
from ..core.db import DB_SESSION
from ..model.authentication import Admin
import json
csg_router = APIRouter(prefix="/api/v1/csg")

# Category Routes
@csg_router.post("/create_category") 
async def create_category(
                        # current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        session: DB_SESSION,
                        category_input: Annotated[str, Form(...)],
                        category_image: UploadFile = File(...),
                        ):
    """
    Create a new product in the database.

    Args:
        {
    "category_name": "string",
    "category_desc": "string"
}
    """
    try: 
        category_dict = json.loads(category_input)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data provided for product details")

    category_base_model = CategoryBaseModel(**category_dict)
    category = await create_categories(category_base_model, session,  category_image)
    return {"message": "Create Product Category Successfully!", "data" : category}

@csg_router.get("/get_category")
async def get_category(
    # current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
    session: DB_SESSION):
    category = await get_categories(session)
    return category

@csg_router.put("/update_category/{category_id}")
async def update_category(category_id: int, 
                        session: DB_SESSION,
                        # current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],,
                        category_input: Annotated[str, Form(...)],
                        image: UploadFile = File(...),
                        ):
    """
    Create a new product in the database.

    Args:
        {
    "category_name": "string",
    "category_desc": "string"
}
    """
    try:
        category_dict = json.loads(category_input)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data provided for product details")

    category_base_model = CategoryBaseModel(**category_dict)
    category = await update_categories(category_id, category_base_model, session, image)
    return {"message": "Update Product Category Successfully!", "data" : category}


# Size Routes
@csg_router.post("/create_size")
async def create_size(size_input: Size, 
                    # current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION):
    size = await create_sizes(size_input,session)
    return {"message": "Create Product Size Successfully!", "data" : size}

@csg_router.get("/get_sizes")
async def get_sizes(session: DB_SESSION,
                    # current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    ):
    size = await get_sizies(session)
    return size


# Gender Routes
@csg_router.post("/create_gender")
async def create_gender(gender_input: Gender, 
                        # current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        session: DB_SESSION):
    gender = await create_genders(gender_input,session)
    return {"message": "Create Product Genders Successfully!", "data" : gender}

@csg_router.get("/get_genders")
async def get_genders(session: DB_SESSION
# current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
):
    genders = await get_all_genders(session)
    return genders