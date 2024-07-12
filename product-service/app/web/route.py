from ..service.product_service import get_all_product_details, get_specific_product_details, get_product_by_category, deleted_product, create_product, search_product_results
from ..utils.admin_verify import get_current_active_admin_user
from ..model.models import Product, ProductFormModel
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from aiokafka import AIOKafkaProducer # type: ignore
from ..kafka.producer import get_kafka_producer
from typing import Annotated, Optional, List
from ..core.db import DB_SESSION
from ..model.authentication import Admin
from sqlmodel import Session
import json

router = APIRouter(prefix="/api/v1")

@router.post("/create_product")
async def create_products(
                        current_admin: Annotated[Admin, Depends(get_current_active_admin_user)], 
                        aio_producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
                        session: DB_SESSION,
                        product_details: Annotated[str, Form(...)],
                        images: List[UploadFile] = File(...),
                        ):
    """
    Create a new product in the database.

    Args:
        product_details : Annotated[str, Form(...)] = { 
        "product_name": "string", "product_desc": "string", 
        "category_id": int, "gender_id": int, 
        "product_item": [ 
        { "color": "string", 
        "sizes": [ { "size": int, "price": int, "stock": int } ] 
        } ]
        }
    """
    try: 
        product_details_dict = json.loads(product_details)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data provided for product details")

    product_details_model = ProductFormModel(**product_details_dict)
    product = await create_product(current_admin, aio_producer, session, product_details_model, images)
    # product = await create_product(aio_producer, session, product_details_model, images)
    return {"message": "Create Product Successfully!", "data": product}

@router.get("/get_all_products")
async def get_all_product(session: DB_SESSION):
    products = await get_all_product_details(session)
    return products

# specific_product details
@router.get("/product/{product_id}")
async def specific_product_details(product_id: str, session: DB_SESSION):
    product = await get_specific_product_details(product_id, session)
    return product

# search_product_results 
@router.get("/search_product/{input}")
async def search_product(input:str, session: DB_SESSION):
    products = await search_product_results(input, session)
    return products

# Products By Category
@router.get("/product_by_category/{category}")
async def product_by_category(category:str, session: DB_SESSION):
    products = await get_product_by_category(category, session)
    return products

# Deleted Products
@router.delete("/delete_product/{product_id}")
async def delete_product(product_id:str, 
                        session: DB_SESSION,
                        current_admin: Annotated[Admin, Depends(get_current_active_admin_user)]
                        ):
    product = await deleted_product(product_id, current_admin, session)
    return product