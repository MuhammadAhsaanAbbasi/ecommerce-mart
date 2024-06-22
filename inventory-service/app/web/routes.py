from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from typing import Annotated, Optional, List
from ..utils.admin_verify import get_current_active_admin_user
from ..model.admin import Admin
from ..model.models import Product, ProductSize, ProductItem, ProductItemFormModel, SizeModel, Stock
from ..core.db import DB_SESSION
from sqlmodel import Session
import json

router = APIRouter(prefix="/api/v1/inventory")

# Product Item Routes
@router.post("/product_item")
async def create_product_items(current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    product_item_detail: ProductItemFormModel,
                    image: UploadFile = File(...)
                    ):
    # product_item = await create_product_item(current_admin, session, product_item_detail, image)
    return {"message" : "Item of Product Create Successfully!"}

@router.get("/product_item")
async def get_product_items(current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    product_id: int):
    # product_items = await get_product_item(current_admin, session, product_id)
    return {"message" : "Item of Product Get Successfully!"}

@router.delete("/product_item")
async def delete_product_items(current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    product_item_id: int):
    #product_item = await delete_product_item(current_admin, session, product_item_id)
    return {"message" : "Item of Product Delete Successfully!"}

@router.post("/product_Size")
async def product_sizes(current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        session: DB_SESSION,
                        product_size_detail: SizeModel,
                        product_item_id: int
                        ):
    # product_size = await create_product_size(current_admin, session, product_size_detail, product_item_id)
    return {"message" : "Size of Product Create Successfully!"}

@router.get("/product_Size")
async def get_product_sizes(current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        session: DB_SESSION,
                        product_item_id: int):
    # product_sizes = await get_product_size(current_admin, session, product_item_id)
    return {"message" : "Size of Product Get Successfully!"}

@router.delete("/product_Size")
async def delete_product_sizes(current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        session: DB_SESSION,
                        product_size_id: int):
    #product_size = await delete_product_size(current_admin, session, product_size_id)
    return {"message" : "Size of Product Delete Successfully!"}

@router.put("/product_Size")
async def update_product_sizes(current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        session: DB_SESSION,
                        product_size_detail: SizeModel,
                        product_size_id: int):
    #product_size = await update_product_size(current_admin, session, product_size_detail, product_size_id)
    return {"message" : "Size of Product Update Successfully!"}