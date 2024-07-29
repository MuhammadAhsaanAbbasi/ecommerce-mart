from ..utils.action import create_categories, get_categories, create_sizes, get_sizies, update_categories, update_color
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from ..model.category_model import Category, Size, CategoryBaseModel
from ..utils.admin_verify import get_current_active_admin_user
from ..model.authentication import Admin
from ..model.models import Color
from ..core.db import DB_SESSION
from typing import Annotated, Optional
from sqlmodel import select
import json

csc_router = APIRouter(prefix="/api/v1/csc")

# Category Routes
@csc_router.post("/category/create") 
async def create_category(
                        current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        session: DB_SESSION,
                        category_input: Annotated[str, Form(...)],
                        category_image: UploadFile = File(...),
                        ):
    """
    Create a new product in the database.

    Args:
        {
    "category_name": "string",
    "category_desc": "string",
    "category_type":  formal = "formal"   casual = "casual"     luxury = "luxury" 
    
    """
    try: 
        category_dict = json.loads(category_input)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data provided for product details")

    category_base_model = CategoryBaseModel(**category_dict)
    category = await create_categories(category_base_model, current_admin, session, category_image)
    # category = await create_categories(category_base_model, session, category_image)
    return {"message": "Create Product Category Successfully!", "data" : category}

@csc_router.get("/categories/all")
async def get_category(session: DB_SESSION):
    category = await get_categories(session)
    return category

@csc_router.get("/category/{category_id}")
async def get_specific_category(category_id: str, 
                        session: DB_SESSION):
    category = session.exec(select(Category).where(Category.id == category_id)).first()
    if not category:
        raise HTTPException(status_code=404, detail="Product not found")
    return category

@csc_router.put("/update_category/{category_id}")
async def update_category(category_id: str, 
                        session: DB_SESSION,
                        current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        category_input: Annotated[str, Form(...)],
                        image: Optional[UploadFile] = None,
                        ):
    """
    Create a new product in the database.

    Args:
        {
    "category_name": "string",
    "category_desc": "string"
    "category_type":  formal = "formal"   casual = "casual"     luxury = "luxury"
        }
    """
    try:
        category_dict = json.loads(category_input)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data provided for product details")

    category_base_model = CategoryBaseModel(**category_dict)
    category = await update_categories(category_id, category_base_model, current_admin, session, image) 
    return category

@csc_router.delete("/delete_category/{category_id}")
async def delete_category(category_id: str, 
                        current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        session: DB_SESSION):
    if not current_admin:
        raise HTTPException(status_code=401, detail="Unauthorized Admin")

    category = session.exec(select(Category).where(Category.id == category_id)).first()

    session.delete(category)
    session.commit()

    return {"message": "Delete Product Category Successfully!"}

# Size Routes
@csc_router.post("/size")
async def create_size(size_input: Size, 
                    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION):
    size = await create_sizes(size_input, current_admin, session)
    # size = await create_sizes(size_input, session)
    return {"message": "Create Product Size Successfully!", "data" : size}

@csc_router.get("/sizes")
async def get_sizes(session: DB_SESSION):
    size = await get_sizies(session)
    return size

@csc_router.delete('/size/{size_id}')
async def delete_size(size_id: str, 
                        current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        session: DB_SESSION):
    if not current_admin:
        raise HTTPException(status_code=401, detail="Unauthorized Admin")
    
    size = session.exec(select(Size).where(Size.id == size_id)).first()
    if not size:
        raise HTTPException(status_code=404, detail="Size not found")
    
    session.delete(size)
    session.commit()
    return {"message": "Delete Product Size Successfully!"}

# Color Routes
@csc_router.post('/color/create')
async def create_colors(color_details: Color, 
                        # current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        session: DB_SESSION):
    # if not current_admin:
    #     raise HTTPException(status_code=401, detail="Unauthorized Admin")
    
    color = Color(**color_details.model_dump())
    session.add(color)
    session.commit()
    session.refresh(color)
    return {"Message": "Create Color", "details": color}

@csc_router.get('/colors')
async def get_colors(session: DB_SESSION,
                    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],):
    if not current_admin:
        raise HTTPException(status_code=401, detail="Unauthorized Admin")
    
    colors = session.exec(select(Color)).all()
    return {"data" : colors}

@csc_router.get("/color/{color_id}")
async def get_specific_color (color_id: str, 
                        session: DB_SESSION,
                        current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        ):
    if not current_admin:
        raise HTTPException(status_code=401, detail="Unauthorized Admin")
    
    color = session.exec(select(Color).where(Color.id == color_id)).first()
    if not color:
        raise HTTPException(status_code=404, detail="Product not found")
    return color

@csc_router.put('/color/{color_id}')
async def update_colors(color_id: str,
                        color_details: Color,
                        current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        session: DB_SESSION):
    color = await update_color(color_id, color_details, current_admin, session)
    return color

@csc_router.delete('/color/{color_id}')
async def delete_color(color_id: str, 
                    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION):
    if not current_admin:
        raise HTTPException(status_code=401, detail="Unauthorized Admin")
    
    color = session.exec(select(Color).where(Color.id == color_id)).first()
    if not color:
        raise HTTPException(status_code=404, detail="Color not found")
    
    session.delete(color)
    session.commit()
    return {"message": "Delete Product Color Successfully!"}