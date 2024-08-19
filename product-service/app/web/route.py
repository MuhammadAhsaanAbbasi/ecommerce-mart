from ..service.product_service import get_all_product_details, get_specific_product_details, get_product_by_category, deleted_product, create_product, search_product_results, updated_product, get_new_arrivals_details, may_also_like_products_details, get_features_product
from ..model.models import ProductBaseForm, ProductFormModel
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from ..utils.admin_verify import get_current_active_admin_user
from aiokafka import AIOKafkaProducer # type: ignore
from typing import Annotated, Optional, List, Dict
from ..model.authentication import Admin, Users
from ..kafka.producer import get_kafka_producer
from ..core.db import DB_SESSION
import json
import uuid

router = APIRouter(prefix="/api/v1/product")

@router.post("/create")
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
        "product_name": "string", "product_desc": "string",  "featured": True
        "category_id": "id",
        "product_item": [ 
        { "color": "color_id", 
        "sizes": [ { "size": "id", "price": int, "stock": int } ] 
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


# specific_product details
@router.get("/specific/{product_id}")
async def specific_product_details(product_id: str, session: DB_SESSION):
    product = await get_specific_product_details(product_id, session)
    return product


# Featured Product
@router.get('/featured')
async def get_featured_products(session: DB_SESSION,
                            page: int = 1, 
                            page_size: int = 16, 
                            sort_by: str = 'created_at', 
                            sort_order: str = 'desc'
                        ):
    product = await get_features_product(session, page, page_size, sort_by, sort_order )
    return product


# search_product_results 
@router.get("/search/{input}")
async def search_product(input:str, session: DB_SESSION):
    products = await search_product_results(input, session)
    return products


# Products By Category
@router.get("/gets/{input}")
async def product_by_category(input:str, 
                            session: DB_SESSION,
                            page: int = 1, 
                            page_size: int = 16, 
                            sort_by: str = 'created_at', 
                            sort_order: str = 'desc',
                            ):
    if input == 'all':
        products = await get_all_product_details(session, page, page_size, sort_by, sort_order)
    elif input == "new-arrivals":
        products = await get_new_arrivals_details(session, page, page_size, sort_by, sort_order)
    else:
        products = await get_product_by_category(input, session, page, page_size, sort_by, sort_order)
    return products


# Update Product
@router.put("/update/{product_id}")
async def update_product(product_id:str,
                        product_input: ProductBaseForm,
                        session: DB_SESSION,
                        current_admin: Annotated[Admin, Depends(get_current_active_admin_user)]
                        ):
    """
    Search for products by input in both category and product tables.

    Args:
        input (str): The input to search for in category and product names.
        session (DB_SESSION): The database session.
    """
    product = await updated_product(product_id, product_input, session, current_admin)
    # product = await updated_product(product_id, product_input, session)
    return product


# Deleted Products
@router.delete("/delete/{product_id}")
async def delete_product(product_id:str, 
                        session: DB_SESSION,
                        current_admin: Annotated[Admin, Depends(get_current_active_admin_user)]
                        ):
    product = await deleted_product(product_id, current_admin, session)
    # product = await deleted_product(product_id, session)
    return product

#  You May Also Like Products
@router.get("/may-also-like/{product_id}")
async def may_also_like_products(product_id: str, session: DB_SESSION):
    products = await may_also_like_products_details(product_id, session)
    return  products