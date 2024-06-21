from typing import Annotated, Optional, Union, List
import cloudinary.uploader # type: ignore
from ..setting import CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, CLOUDINARY_CLOUD
from fastapi import Depends, HTTPException, UploadFile, File, Form
from sqlmodel import select, func
from ..core.db import DB_SESSION
from ..model.models import Product, ProductSize, ProductItem, Stock, ProductFormModel
from ..model.category_model import Category
from ..utils.admin_verify import get_current_active_admin_user
from ..utils.utils import search_algorithm_by_category
from ..model.admin import Admin
import cloudinary # type: ignore
from sqlalchemy import or_

# Configuration       
cloudinary.config( 
    cloud_name = CLOUDINARY_CLOUD, 
    api_key = CLOUDINARY_API_KEY, 
    api_secret = CLOUDINARY_API_SECRET, # Click 'View Credentials' below to copy your API secret
    secure=True
)

# Create Product
async def create_product(
                # current_admin: Annotated[Admin, Depends(get_current_active_admin_user)], 
                session: DB_SESSION,
                product_details:ProductFormModel,
                images: List[UploadFile] = File(...),
                ):
    """
    Create a new product in the database.

    Args:
        product_details (ProductFormModel): Details of the product to be created.
        session (Annotated[Session, Depends(get_session)]): Database session for performing operations.
        admin_verification (Annotated[Admin, Depends(get_current_active_admin_user)]): Admin verification dictionary obtained via dependency injection.
        images (List[UploadFile]): List of images to be uploaded.

    Raises:
        HTTPException: If the user is not an admin.
        HTTPException: If the number of images does not match the number of product items.
        HTTPException: If product details are not provided.
        HTTPException: If an error occurs during image upload.
        HTTPException: If an error occurs while creating the product.

    Returns:
        Product: The created product.
    """
    # if not current_admin:
    #     raise HTTPException(status_code=404,
    #                         detail="Admin not found")
    
    if len(product_details.product_item) != len(images):
        raise HTTPException(status_code=202, detail="The number of images does not match the number of product items")
    
    if not product_details:
        raise HTTPException(status_code=400, detail="Product details not provided")

    product_item_tables: List[ProductItem] = []
    try:
        for product_items, image in zip(product_details.product_item, images):
            try:
                upload_result = cloudinary.uploader.upload(image.file)
                image_url = upload_result["secure_url"]
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error Occurs during image upload: {e}")
            
            product_size_tables: List[ProductSize] = []
            for product_size in product_items.sizes:
                stock_tables = Stock(stock=product_size.stock)
                product_size_schema = ProductSize(size=product_size.size, price=product_size.price, stock=stock_tables)
                product_size_tables.append(product_size_schema)
            
            product_item = ProductItem(color=product_items.color, image_url=image_url, sizes=product_size_tables)
            product_item_tables.append(product_item)
        
        product = Product(
            product_name=product_details.product_name,
            product_desc=product_details.product_desc,
            category_id=product_details.category_id,
            gender_id=product_details.gender_id,
            product_item=product_item_tables
        )
        
        session.add(product)
        session.commit()
        session.refresh(product)

        return product
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error Occurs while creating the product: {e}")



# get all product details
async def get_all_product_details(session: DB_SESSION):
    products = session.exec(select(Product)).all()
    return {"data" : products}

# get specific product details
async def get_specific_product_details(product_id: int, session: DB_SESSION):
    product = session.exec(select(Product).where(Product.id == product_id)).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"data" : product}

# search_product_results
async def search_product_results(input: str, session: DB_SESSION):
    """
    Search for products by input in both category and product tables.

    Args:
        input (str): The input to search for in category and product names.
        session (DB_SESSION): The database session.

    Returns:
        List[Product]: A list of products that match the input.
    """
    categories = await search_algorithm_by_category(input, session)
        
    if categories:
        categories_ids = [category.id for category in categories]

        # Use or_ to combine multiple conditions
        conditions = [Product.category_id == category_id for category_id in categories_ids]
        category_products = session.exec(select(Product).where(or_(*conditions))).all()
    else:
        category_products = []

    # Search for products that start with the input
    products = session.exec(select(Product).where(Product.product_name.startswith(input))).all()
    
    # Collect unique product IDs
    category_product_ids = {product.id for product in category_products if product.id is not None}
    product_ids = {product.id for product in products if product.id is not None}

    # Combine the unique product IDs
    unique_product_ids = category_product_ids.union(product_ids)

    # Fetch the unique products from the database
    unique_products = session.exec(select(Product).where(Product.id.in_(unique_product_ids))).all() # type: ignore

    return {"data": unique_products}



# get product by category
async def get_product_by_category(catogery:str, session: DB_SESSION):
    category = session.exec(select(Category).where(Category.category_name == catogery)).first()

    if not category:
        raise HTTPException(status_code=404,
                            detail="Category not found")
    
    products = session.exec(select(Product).where(Product.category_id == category.id)).all()
    return {"data" : products}

# delete product
async def deleted_product(product_id:int, current_admin: Annotated[Admin, Depends(get_current_active_admin_user)], session: DB_SESSION):
    if not current_admin:
        raise HTTPException(status_code=404,
                            detail="Admin not found")
    
    product = session.exec(select(Product).where(Product.id == product_id)).first()
    if not product:
        raise HTTPException(status_code=404,
                            detail="Product not found")
    
    session.delete(product)
    session.commit()
    session.refresh(product)

    return {"data" : product}

