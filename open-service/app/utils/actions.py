from ..model.product import Product, ProductItem, ProductSize, Stock, SizeModel, ProductItemFormModel, ProductFormModel, Size, Category
from ..utils.admin_verify import get_current_active_admin_user
from ..utils.user_verify import get_current_active_user
from fastapi import Depends, HTTPException, Query
from ..model.authentication import Users, Admin
from typing import Annotated, Optional, List, Sequence
from ..core.db import DB_SESSION
from datetime import datetime
from sqlmodel import select
import json 
import uuid

async def get_categories(session: DB_SESSION):
    categories = session.exec(select(Category)).all()
    return {"data" : categories}

async def all_product_details(products: Sequence[Product], session: DB_SESSION):
    all_product_detail = []

    for product in products:
        product_items = session.exec(select(ProductItem).where(ProductItem.product_id == product.id)).all()
        product_items_table: List[ProductItemFormModel] = []

        for item in product_items:
            product_sizes = session.exec(select(ProductSize).where(ProductSize.product_item_id == item.id)).all()
            product_sizes_table: List[SizeModel] = []

            for product_size in product_sizes:
                size = session.exec(select(Size).where(Size.id == product_size.size)).first()
                if not size:
                    raise HTTPException(status_code=404, detail="Size not found")
                stock = session.exec(select(Stock).where(Stock.product_size_id == product_size.id)).first()
                if stock and stock.stock > 0:
                    size_model = SizeModel(
                        id=product_size.id,
                        product_size_id=product_size.product_size_id, 
                        size=size.size,
                        price=product_size.price,
                        stock=stock.stock
                    )
                    product_sizes_table.append(size_model)
            
            if product_sizes_table:
                product_item_model = ProductItemFormModel(
                    id=item.id,
                    product_item_id=item.product_item_id,
                    color=item.color,
                    image_url=item.image_url,
                    sizes=product_sizes_table
                )
                product_items_table.append(product_item_model)

        product_details = ProductFormModel(
                product_id=product.product_id,
                product_name=product.product_name,
                product_desc=product.product_desc,
                category_id=product.category_id,
                gender_id=product.gender_id,
                product_item=product_items_table
            )
        all_product_detail.append(product_details)

    return all_product_detail