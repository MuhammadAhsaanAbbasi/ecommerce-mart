from ..model.product import Product, ProductFormModel, ProductItem, ProductItemFormModel, ProductSize, Size, SizeModel, Category, CategoryType
from ..service.open_service import get_features_product, get_all_product_details, get_orders_by_tracking_id, get_openai_shop_assistant # type: ignore 
from fastapi import APIRouter, Response, HTTPException
from ..core.db import DB_SESSION
from datetime import datetime
from sqlmodel import select
from typing import List, Sequence
import random


router = APIRouter(prefix="/api/v1")

@router.get('/products/featured/')
async def get_featured_products(session: DB_SESSION,
                            page: int = 1, 
                            page_size: int = 16, 
                            sort_by: str = 'created_at', 
                            sort_order: str = 'desc'
                        ):
    product = await get_features_product(session, page, page_size, sort_by, sort_order )
    return product

@router.get("/category/{category_type}")
async def get_specific_category(category_type: str, 
                        session: DB_SESSION):
    category = session.exec(select(Category).where(Category.category_type == category_type)).all()
    if not category:
        raise HTTPException(status_code=404, detail="Product not found")
    return category


@router.get("/category/shuffles", response_model=List[Category])
async def get_shuffle_categories(session: DB_SESSION):
    # Fetch categories by type and convert to lists
    formal_categories = list(session.exec(select(Category).where(Category.category_type == CategoryType.formal)).all())
    casual_categories = list(session.exec(select(Category).where(Category.category_type == CategoryType.casual)).all())
    luxury_categories = list(session.exec(select(Category).where(Category.category_type == CategoryType.luxury)).all())

    # Ensure there are at least 2 categories of each type
    if len(formal_categories) < 2 or len(casual_categories) < 2 or len(luxury_categories) < 2:
        raise HTTPException(status_code=404, detail="Not enough categories of each type to perform shuffle")

    # Shuffle and select 2 categories from each type
    random.shuffle(formal_categories)
    random.shuffle(casual_categories)
    random.shuffle(luxury_categories)

    selected_categories = (
        formal_categories[:2] +
        casual_categories[:2] +
        luxury_categories[:2]
    )

    # Shuffle the combined list
    random.shuffle(selected_categories)

    return selected_categories

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