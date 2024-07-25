from ..model.product import Color, Product, ProductItem, ProductSize, Stock, Size, Category, SizeModelDetails, ProductDetails, ProductItemDetails, ProductAssistFormModel, ProductItemAssistFormModel, SizeModelForm
from fastapi import Depends, HTTPException, Query
from ..model.authentication import Users, Admin
from typing import Annotated, Optional, List, Sequence
from ..core.db import DB_SESSION
from datetime import datetime
from sqlmodel import select


async def get_categories(session: DB_SESSION):
    categories = session.exec(select(Category)).all()
    return {"data" : categories}

async def all_product_details(products: Sequence[Product], session: DB_SESSION):
    all_product_detail = []

    for product in products:
        product_items = session.exec(select(ProductItem).where(ProductItem.product_id == product.id)).all()
        product_items_table: List[ProductItemDetails] = []

        for item in product_items:
            product_sizes = session.exec(select(ProductSize).where(ProductSize.product_item_id == item.id)).all()
            product_sizes_table: List[SizeModelDetails] = []

            for product_size in product_sizes:
                size = session.exec(select(Size).where(Size.id == product_size.size)).first()
                if not size:
                    raise HTTPException(status_code=404, detail="Size not found")
                stock = session.exec(select(Stock).where(Stock.product_size_id == product_size.id)).first()
                if stock and stock.stock > 0:
                    size_model = SizeModelDetails(
                        product_size_id=product_size.id,
                        size=size.size,
                        price=product_size.price,
                        stock=stock.stock
                    )
                    product_sizes_table.append(size_model)

            if product_sizes_table:
                color = session.exec(select(Color).where(Color.id == item.color)).first()
                if not color:
                    raise HTTPException(status_code=404, detail="Color not found")

                product_item_model = ProductItemDetails(
                    product_item_id=item.id,
                    color_name=color.color_name,
                    color_value=color.color_value,
                    color=item.color,
                    image_url=item.image_url,
                    sizes=product_sizes_table
                )
                product_items_table.append(product_item_model)

        product_details = ProductDetails(
            product_id=product.id,
            product_name=product.product_name,
            product_desc=product.product_desc,
            featured=product.featured,
            category_id=product.category_id,
            product_item=product_items_table
        )
        all_product_detail.append(product_details)

    return all_product_detail

async def single_product_details(product_name: str, session: DB_SESSION):
    product = session.exec(select(Product).where(Product.product_name == product_name)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product_items = session.exec(select(ProductItem).where(ProductItem.product_id == product.id)).all()
    product_items_table: List[ProductItemAssistFormModel] = []

    for item in product_items:
        product_sizes = session.exec(select(ProductSize).where(ProductSize.product_item_id == item.id)).all()
        product_sizes_table: List[SizeModelForm] = []

        for product_size in product_sizes:
            size = session.exec(select(Size).where(Size.id == product_size.size)).first()
            if not size:
                raise HTTPException(status_code=404, detail="Size not found")
            size_model = SizeModelForm(
                        size=size.size,
                        price=product_size.price,
                    )
            product_sizes_table.append(size_model)
            color = session.exec(select(Color).where(Color.id == item.color)).first()
            if not color:
                raise HTTPException(status_code=404, detail="Color not found")

            product_item_model = ProductItemAssistFormModel(
                    color_name=color.color_name,
                    sizes=product_sizes_table
                )
            product_items_table.append(product_item_model)

        product_details = ProductAssistFormModel(
                product_name=product.product_name,
                product_desc=product.product_desc,
                product_item=product_items_table
            )
        
        return product_details
