from typing import Annotated, Optional, Union, List
import cloudinary.uploader # type: ignore
from ..setting import CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, CLOUDINARY_CLOUD
from fastapi import Depends, HTTPException, UploadFile, File, Form
from sqlmodel import Session, select
from ..core.db import get_session
from ..model.models import Product, ProductSize, ProductItem, Stock, ProductFormModel
from ..model.category_model import Category
from ..utils.admin_verify import get_current_active_admin_user
from ..model.admin import Admin
import cloudinary # type: ignore

# Configuration       
cloudinary.config( 
    cloud_name = CLOUDINARY_CLOUD, 
    api_key = CLOUDINARY_API_KEY, 
    api_secret = CLOUDINARY_API_SECRET, # Click 'View Credentials' below to copy your API secret
    secure=True
)

# Create Product
async def create_product(
                current_admin: Annotated[Admin, Depends(get_current_active_admin_user)], 
                session: Annotated[Session, Depends(get_session)],
                product_details:ProductFormModel,
                images: List[UploadFile] = File(...),
                ):
    """
    Create a new product in the database.

    Args:
        product_details (ProductFormModel): Details of the product to be created.
        session (DB_SESSION): Database session for performing operations.
        admin_verification (dict): Admin verification dictionary obtained via dependency injection.
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
    if not current_admin:
        raise HTTPException(status_code=404,
                            detail="Admin not found")
    
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
async def get_all_product_details(session: Annotated[Session, Depends(get_session)]):
    products = session.exec(select(Product)).all()
    return {"data" : products}

# get specific product details
async def get_specific_product_details(product_id: int, session: Annotated[Session, Depends(get_session)]):
    product = session.exec(select(Product).where(Product.id == product_id)).first()
    return {"data" : product}

# search_product_results
async def search_product_results(details:str, session:Annotated[Session, Depends(get_session)]):
    return {"": ""}

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