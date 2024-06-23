from ..service.inventory_service import create_product_item, get_product_item, delete_product_item, create_product_size, get_product_size, delete_product_size, update_product_item_size
from ..model.models import Product, ProductSize, ProductItem, ProductItemFormModel, SizeModel, Stock
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from ..utils.admin_verify import get_current_active_admin_user
from typing import Annotated, Optional, List
from ..core.db import DB_SESSION
from ..model.admin import Admin
import json

router = APIRouter(prefix="/api/v1/inventory")

# Product Item Routes
@router.post("/create_product_item")
async def create_product_items(
    # current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
    session: DB_SESSION,
    product_id: int,
    product_item_details: Annotated[str, Form(...)],
    image: UploadFile = File(...),
):
    """
    Create a new product item in the database.

    Args:
        product_item_details: Annotated[str, Form(...)] = {
        "color": "string", 
        "product_id": int,
        "sizes": [ { "size": int, "price": int, "stock": int } ] 
        }
    """
    try:
        product_item_details_dict = json.loads(product_item_details)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data provided for product item details")

    product_item_details_model = ProductItemFormModel(**product_item_details_dict)
    # product_item = await create_product_item(current_admin, session, product_id, product_item_details_model, image)
    product_item = await create_product_item(session, product_id, product_item_details_model, image)
    return {"message": "Create Product Item Successfully!", "data": product_item}

@router.get("/product_item")
async def get_product_items(
                    # current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    product_id: int):
    # product_items = await get_product_item(current_admin, session, product_id)
    product_items = await get_product_item(session, product_id)
    return {"message" : "Item of Product Get Successfully!", "data" : product_items}

@router.delete("/product_item")
async def delete_product_items(
                    #  current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    product_item_id: int):
    # product_item = await delete_product_item(current_admin, session, product_item_id)
    product_item = await delete_product_item(session, product_item_id)
    return {"message" : "Item of Product Delete Successfully!", "data" : product_item}

# Product Size 
@router.post("/product_size")
async def create_product_sizes(
                        # current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        session: DB_SESSION,
                        product_size_detail: SizeModel,
                        product_item_id: int
                        ):
    # product_size = await create_product_size(current_admin, session, product_size_detail, product_item_id)
    product_size = await create_product_size(session, product_size_detail, product_item_id)
    return {"message" : "Size of Product Create Successfully!", "data" : product_size }

@router.get("/product_size")
async def get_product_sizes(
                        # current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        session: DB_SESSION,
                        product_item_id: int):
    # product_sizes = await get_product_size(current_admin, session, product_item_id)
    product_sizes = await get_product_size(session, product_item_id)
    return {"message" : "Size of Product Get Successfully!", "data" : product_sizes }

@router.delete("/product_size")
async def delete_product_sizes(
                        # current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        session: DB_SESSION,
                        product_size_id: int):
    # product_size = await delete_product_size(current_admin, session, product_size_id)
    product_size = await delete_product_size(session, product_size_id)
    return {"message" : "Size of Product Delete Successfully!", "data" : product_size}

# Update Product Item
@router.put("/update_product_item")
async def update_product_item_sizes(
    # current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
    session: DB_SESSION,
    product_item_details: Annotated[str, Form(...)],
    product_item_id: int,
    image: Optional[UploadFile] = File(None),
):
    """
    Update an existing product item in the database.

    Args:
        product_item_details: Annotated[str, Form(...)] = {
        "color": "string", 
        "sizes": [ { "size": int, "price": int, "stock": int } ] 
        }
    """
    try:
        product_item_details_dict = json.loads(product_item_details)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data provided for product item details")

    product_item_details_model = ProductItemFormModel(**product_item_details_dict)
    # product_item = await update_product_item_size(current_admin, session, product_item_details_model, product_item_id, image)
    product_item = await update_product_item_size(session, product_item_details_model, product_item_id, image)
    return {"message": "Update Product Item Successfully!", "data": product_item}
