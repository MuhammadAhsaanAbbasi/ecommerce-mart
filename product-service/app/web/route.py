from ..service.product_service import get_all_product_details, get_specific_product_details, get_product_by_category, deleted_product, create_product, search_product_results
from ..utils.admin_verify import get_current_active_admin_user
from ..model.models import Product, ProductFormModel
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from typing import Annotated, Optional, List
from ..core.db import get_session
from ..model.admin import Admin
from sqlmodel import Session
import json

router = APIRouter(prefix="/api/v1")

@router.post("/create_product")
async def create_products(
                        current_admin: Annotated[Admin, Depends(get_current_active_admin_user)], 
                        session: Annotated[Session, Depends(get_session)],
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
    product = await create_product(current_admin, session, product_details_model, images)
    return {"message": "Create Product Successfully!", "data": product}

@router.get("/get_all_products")
async def get_all_product(session: Annotated[Session, Depends(get_session)]):
    products = get_all_product_details(session)
    return {"message": "Get Product Details"}

# specific_product details
@router.get("/product/{product_id}")
async def specific_product_details(product_id: int, session: Annotated[Session, Depends(get_session)]):
    product = get_specific_product_details(product_id, session)
    return {"message" : "specific product details"}

@router.get("/search_product/{details}")
async def search_product(details:str, session:Annotated[Session, Depends(get_session)]):
    products = search_product_results(details, session)
    return {"message" : "search product details"}

@router.get("/product_by_category/{category}")
async def product_by_category(category:str, session:Annotated[Session, Depends(get_session)]):
    products = get_product_by_category(category, session)
    return {"message" : "category product details"}

@router.delete("/delete_product/{product_id}")
async def delete_product(product_id:int, current_admin: Annotated[Admin, Depends(get_current_active_admin_user)], session:Annotated[Session, Depends(get_session)]):
    product = deleted_product(product_id, current_admin, session)
    return {"message" : "delete product"}