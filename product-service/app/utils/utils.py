from ..model.models import Product, ProductSize, ProductItem, Stock, ProductFormModel, ProductItemFormModel, SizeModel
from ..model.category_model import Category, Size, Gender, CategoryBaseModel
from typing import List, Sequence, Annotated
from sqlmodel import SQLModel, select, Session
from ..core.db import DB_SESSION
from ..core.config import upload_files_in_s3
from fastapi import HTTPException, UploadFile, File, Form

# Create Categories
async def create_categories(category_input: CategoryBaseModel,
                            # current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                            session: DB_SESSION,
                            image: UploadFile = File(...)):
    category_image = await upload_files_in_s3(image)
    category = Category(**category_input.model_dump(), category_image=category_image)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

# Get Categories
async def get_categories(session: DB_SESSION):
    categories = session.exec(select(Category)).all()
    return {"data" : categories}

async def update_categories(category_id: int, 
                        category_input: CategoryBaseModel,
                        # current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        session: DB_SESSION,
                        image: UploadFile = File(...),
                        ):
    # if not current_admin:
    #     raise HTTPException(status_code=401, detail="Unauthorized Admin")

    category_image = await upload_files_in_s3(image)

    category = session.exec(select(Category).where(Category.id == category_id)).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category_data = category_input.model_dump()
    for field, value in category_data.items():
        setattr(category, field, value)
        if field == "category_image":
            category.category_image = category_image
    
    session.commit()
    session.refresh(category)

    return {"message" : "Update Categories Successfully!"}

# Create Size
async def create_sizes(size_input: Size,
                        # current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        session: DB_SESSION):
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
async def create_genders(gender_input: Gender,
                        # current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        session: DB_SESSION):
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
            product_sizes = session.exec(select(ProductSize).where(ProductSize.product_item_id == item.id)).all()
            product_sizes_table: List[SizeModel] = []

            for product_size in product_sizes:
                size = session.exec(select(Size).where(Size.id == product_size.size)).first()
                if not size:
                    raise HTTPException(status_code=404, detail="Size not found")
                stock = session.exec(select(Stock).where(Stock.product_size_id == product_size.id)).first()
                if stock and stock.stock > 0:
                    size_model = SizeModel(
                        id=product_size.product_size_id,
                        size=size.size,
                        price=product_size.price,
                        stock=stock.stock
                    )
                    product_sizes_table.append(size_model)
            
            if product_sizes_table:
                product_item_model = ProductItemFormModel(
                    id=item.product_item_id,
                    color=item.color,
                    image_url=item.image_url,
                    sizes=product_sizes_table
                )
                product_items_table.append(product_item_model)

        product_details = ProductFormModel(
                id=product.product_id,
                product_name=product.product_name,
                product_desc=product.product_desc,
                category_id=product.category_id,
                gender_id=product.gender_id,
                product_item=product_items_table
            )
        all_product_detail.append(product_details)

    return all_product_detail