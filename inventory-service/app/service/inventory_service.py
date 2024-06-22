from ..model.models import Product, ProductSize, ProductItem, ProductItemFormModel, SizeModel, Stock
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from ..utils.admin_verify import get_current_active_admin_user
from typing import Annotated, Optional, List
from ..model.admin import Admin
from ..core.db import DB_SESSION
from sqlmodel import select

# Product Item
async def create_product_item(current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    product_item_detail: ProductItemFormModel,
                    image: UploadFile = File(...)
                    ):
    return {"message" : "create product items"}

async def get_product_item(current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    product_id: int):
    return {"message" : "get product items"}

async def delete_product_item(current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    product_item_id: int):
    return {"message" : "delete product items"}

# Product Sizes
async def create_product_size(current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        session: DB_SESSION,
                        product_size_detail: SizeModel,
                        product_item_id: int
                        ):
    return {"message" : "create product size"}

async def get_product_size(current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        session: DB_SESSION,
                        product_item_id: int):
    return {"message" : "get product size"}

async def delete_product_size(current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        session: DB_SESSION,
                        product_size_id: int):
    return {"message" : "delete product size"}

async def update_product_size(current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        session: DB_SESSION,
                        product_size_detail: SizeModel,
                        product_size_id: int):
    return {"message" : "update product size"}