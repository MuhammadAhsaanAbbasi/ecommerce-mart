from ..model.product import Product, ProductFormModel, ProductItem, ProductItemFormModel, ProductSize, Size, SizeModel, Category
from ..service.open_service import get_features_product, get_all_product_details, get_orders_by_tracking_id, get_openai_shop_assistant # type: ignore 
from fastapi import APIRouter, Response, HTTPException, Request, Depends, Query
from ..utils.admin_verify import get_current_active_admin_user
from typing import Annotated, Optional, List, Sequence
from ..model.authentication import Users, Admin
from ..utils.actions import get_categories
from ..core.db import DB_SESSION
from datetime import datetime
from sqlmodel import select
import json


router = APIRouter(prefix="/api/v1/open")

@router.get('/new_arrivals')
async def get_featured_products(session: DB_SESSION):
    product = await get_features_product(session)
    return product

@router.get('/all-products')
async def get_all_products(session: DB_SESSION):
    products = await get_all_product_details(session)
    return products

@router.get('/all-categories')
async def get_all_categories(session: DB_SESSION):
    category = await get_categories(session)
    return category

@router.get("/track_order/{tracking_id}")
async def track_order(
                    session: DB_SESSION,
                    tracking_id: str,
                    ):
    order = await get_orders_by_tracking_id(session, tracking_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/shop/assistant")
async def get_shop_assistant_response(session: DB_SESSION, input: str):
    response = await get_openai_shop_assistant(input, session=session)
    return response