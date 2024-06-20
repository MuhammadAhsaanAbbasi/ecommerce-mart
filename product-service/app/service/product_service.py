from typing import Annotated, Optional, Union
from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from ..core.db import get_session
from ..model.models import Product, ProductSize, ProductItem, Stock
from ..model.category_model import Category
from ..utils.admin_verify import get_current_active_admin_user
from ..model.admin import Admin

# Create Product

# get all product details
async def get_all_product_details(session: Annotated[Session, Depends(get_session)]):
    products = session.exec(select(Product)).all()
    return {"data" : products}

# get specific product details
async def get_specific_product_details(product_id: int, session: Annotated[Session, Depends(get_session)]):
    product = session.exec(select(Product).where(Product.id == product_id)).first()
    return {"data" : product}

# get product by category
async def get_product_by_category(catogery:str, session: Annotated[Session, Depends(get_session)]):
    category = session.exec(select(Category).where(Category.category_name == catogery)).first()

    if not category:
        raise HTTPException(status_code=404,
                            detail="Category not found")
    
    products = session.exec(select(Product).where(Product.category_id == category.id)).all()
    return {"data" : products}

# delete product
async def deleted_product(product_id:int, current_admin: Annotated[Admin, Depends(get_current_active_admin_user)], session:Annotated[Session, Depends(get_session)]):
    if not current_admin:
        raise HTTPException(status_code=404,
                            detail="Admin not found")
    product = session.exec(select(Product).where(Product.id == product_id)).first()

    session.delete(product)
    session.commit()
    session.refresh(product)

    return {"data" : product}

