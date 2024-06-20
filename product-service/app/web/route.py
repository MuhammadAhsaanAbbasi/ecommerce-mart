from ..service.product_service import get_all_product_details, get_specific_product_details, get_product_by_category, deleted_product
from ..utils.admin_verify import get_current_active_admin_user
from ..model.models import Product, ProductFormModel
from fastapi import APIRouter, Depends
from typing import Annotated, Optional
from ..core.db import get_session
from ..model.admin import Admin
from sqlmodel import Session

router = APIRouter(prefix="/api/v1")

@router.post("/create_product")
async def create_products(product_details:Product, current_admin: Annotated[Admin, Depends(get_current_active_admin_user)], session: Annotated[Session, Depends(get_session)]):
    # products = create_product(product_details,current_user, session)
    return {"message": "Create Product Details"}

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
    # products = search_product_results(details, session)
    return {"message" : "search product details"}

@router.get("/product_by_category/{category}")
async def product_by_category(category:str, session:Annotated[Session, Depends(get_session)]):
    products = get_product_by_category(category, session)
    return {"message" : "category product details"}

@router.delete("/delete_product/{product_id}")
async def delete_product(product_id:int, current_admin: Annotated[Admin, Depends(get_current_active_admin_user)], session:Annotated[Session, Depends(get_session)]):
    product = deleted_product(product_id, current_admin, session)
    return {"message" : "delete product"}