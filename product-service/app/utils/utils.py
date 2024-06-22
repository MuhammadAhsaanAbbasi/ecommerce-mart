from ..model.models import Product, ProductSize, ProductItem, Stock, ProductFormModel, ProductItemFormModel, SizeModel
from ..model.category_model import Category, Size, Gender
from typing import List, Sequence
from sqlmodel import SQLModel, select, Session
from ..core.db import DB_SESSION
from fastapi import Depends

# Create Categories
async def create_categories(category_input: Category, session: DB_SESSION):
    category = Category(**category_input.model_dump())
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

# Get Categories
async def get_categories(session: DB_SESSION):
    categories = session.exec(select(Category)).all()
    return {"data" : categories}

# Create Size
async def create_sizes(size_input: Size, session: DB_SESSION):
    size = Size(**size_input.model_dump())
    session.add(size)
    session.commit()
    session.refresh(size)
    return size

# Get Sizes
async def get_sizies(session: DB_SESSION):
    sizes = session.exec(select(Size)).all()
    return {"data" : sizes}

# Create Genders
async def create_genders(gender_input: Gender, session: DB_SESSION):
    gender = Gender(**gender_input.model_dump())
    session.add(gender)
    session.commit()
    session.refresh(gender)
    return gender

# Get Genders
async def get_all_genders(session: DB_SESSION):
    genders = session.exec(select(Gender)).all()
    return {"data" : genders}

# Search Algorithm By Category
async def search_algorithm_by_category(input: str, session: DB_SESSION):
    """Search for categories that start with the given input."""
    categories = session.exec(select(Category).where(Category.category_name.startswith(input))).all()
    return categories


async def all_product_details(products: Sequence[Product], session: DB_SESSION):
    all_product_detail = []

    for product in products:
        product_items = session.exec(select(ProductItem).where(ProductItem.product_id == product.id)).all()
        product_items_table: List[ProductItemFormModel] = []

        for item in product_items:
            sizes = session.exec(select(ProductSize).where(ProductSize.product_item_id == item.id)).all()
            product_sizes_table: List[SizeModel] = []

            for size in sizes:
                stock = session.exec(select(Stock).where(Stock.product_size_id == size.id)).first()
                size_stock = stock.stock if stock else 0
                size_model = SizeModel(
                    size=size.size,
                    price=float(size.price),
                    stock=size_stock
                )
                product_sizes_table.append(size_model)
            
            product_item_model = ProductItemFormModel(
                color=item.color,
                image_url=item.image_url,
                sizes=product_sizes_table
            )
            product_items_table.append(product_item_model)

        product_details = ProductFormModel(
            product_name=product.product_name,
            product_desc=product.product_desc,
            category_id=product.category_id,
            gender_id=product.gender_id,
            product_item=product_items_table
        )

        all_product_detail.append(product_details)

    return all_product_detail