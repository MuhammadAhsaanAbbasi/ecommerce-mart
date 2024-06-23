from ..model.models import Product, ProductSize, ProductItem, ProductItemFormModel, SizeModel, Stock
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from ..utils.admin_verify import get_current_active_admin_user
from ..utils.auth import upload_image
from typing import Annotated, Optional, List
from ..model.admin import Admin
from ..core.db import DB_SESSION
from sqlmodel import select


# Create Product Item Function
async def create_product_item(
    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
    session: DB_SESSION,
    product_item_detail: ProductItemFormModel,
    image: UploadFile = File(...)
):
    """
    Create a new product item in the database.

    Args:
        current_admin (Admin): The current authenticated admin.
        session (Session): Database session for performing operations.
        product_item_detail (ProductItemFormModel): Details of the product item to be created.
        image (UploadFile): The image to be uploaded for the product item.

    Raises:
        HTTPException: If the user is not an admin.
        HTTPException: If an error occurs during image upload.
        HTTPException: If an error occurs while creating the product item.

    Returns:
        ProductItem: The created product item.
    """
    if not current_admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    try:
        image_url = upload_image(image)

        product_size_tables: List[ProductSize] = []
        for product_size in product_item_detail.sizes:
            stock_tables = Stock(stock=product_size.stock)
            product_size_schema = ProductSize(size=product_size.size, price=product_size.price, stock=stock_tables)
            product_size_tables.append(product_size_schema)

        product_item = ProductItem(
            color=product_item_detail.color,
            image_url=image_url,
            sizes=product_size_tables
        )

        session.add(product_item)
        session.commit()
        session.refresh(product_item)

        return product_item
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error Occurs while creating the product item: {e}")

async def get_product_item(current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    product_id: int):
    if not current_admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    product_items = session.exec(select(ProductItem).where(ProductItem.product_id == product_id)).all()
    if not product_items:
        raise HTTPException(status_code=404, detail="Product items not found")

    product_item_models = []
    for item in product_items:
        sizes = session.exec(select(ProductSize).where(ProductSize.product_item_id == item.id)).all()
        size_models = []
        for size in sizes:
            stock = session.exec(select(Stock).where(Stock.product_size_id == size.id)).first()
            size_models.append(SizeModel(size=size.size, price=size.price, stock=stock.stock if stock else 0))
        product_item_models.append(ProductItemFormModel(color=item.color, image_url=item.image_url, sizes=size_models))

    return product_item_models

async def delete_product_item(current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    product_item_id: int):
    if not current_admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    product_item = session.exec(select(ProductItem).where(ProductItem.id == product_item_id)).first()
    if not product_item:
        raise HTTPException(status_code=404, detail="Product item not found")

    # Delete related sizes and stock
    sizes = session.exec(select(ProductSize).where(ProductSize.product_item_id == product_item_id)).all()
    for size in sizes:
        stock = session.exec(select(Stock).where(Stock.product_size_id == size.id)).first()
        if stock:
            session.delete(stock)
        session.delete(size)

    session.delete(product_item)
    session.commit()
    return product_item

# Product Sizes
async def create_product_size(
    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
    session: DB_SESSION,
    product_size_detail: SizeModel,
    product_item_id: int
):
    """
    Create a new product size in the database.
    
    Args:
        current_admin (Admin): The current authenticated admin.
        session (Session): Database session for performing operations.
        product_size_detail (SizeModel): Details of the product size to be created.
        product_item_id (int): The ID of the product item to which the size belongs.
    
    Raises:
        HTTPException: If the user is not an admin.
        HTTPException: If the product item is not found.
        HTTPException: If an error occurs while creating the product size.
    
    Returns:
        ProductSize: The created product size.
    """
    if not current_admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    product_item = session.exec(select(ProductItem).where(ProductItem.id == product_item_id)).first()
    if not product_item:
        raise HTTPException(status_code=404, detail="Product item not found")

    try:
        stock_table = Stock(stock=product_size_detail.stock)
        product_size = ProductSize(
            size=product_size_detail.size,
            price=product_size_detail.price,
            stock=stock_table,
            product_item_id=product_item_id
        )

        session.add(product_size)
        session.commit()
        session.refresh(product_size)

        return product_size
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error Occurs while creating the product size: {e}")

async def get_product_size(
    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
    session: DB_SESSION,
    product_item_id: int
):
    """
    Retrieve product sizes for a given product item.

    Args:
        current_admin (Admin): The current authenticated admin.
        session (Session): Database session for performing operations.
        product_item_id (int): The ID of the product item to retrieve sizes for.

    Raises:
        HTTPException: If the user is not an admin.
        HTTPException: If the product item is not found.

    Returns:
        List[ProductSize]: List of product sizes.
    """
    if not current_admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    product_item = session.exec(select(ProductItem).where(ProductItem.id == product_item_id)).first()
    if not product_item:
        raise HTTPException(status_code=404, detail="Product item not found")

    product_sizes = session.exec(select(ProductSize).where(ProductSize.product_item_id == product_item_id)).all()
    return product_sizes

async def delete_product_size(
    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
    session: DB_SESSION,
    product_size_id: int
):
    """
    Delete a product size.

    Args:
        current_admin (Admin): The current authenticated admin.
        session (Session): Database session for performing operations.
        product_size_id (int): The ID of the product size to delete.

    Raises:
        HTTPException: If the user is not an admin.
        HTTPException: If the product size is not found.

    Returns:
        ProductSize: The deleted product size.
    """
    if not current_admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    product_size = session.exec(select(ProductSize).where(ProductSize.id == product_size_id)).first()
    if not product_size:
        raise HTTPException(status_code=404, detail="Product size not found")

    session.delete(product_size)
    session.commit()
    session.refresh(product_size)
    return product_size

async def update_product_item_size(
    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
    session: DB_SESSION,
    product_item_size_detail: ProductItemFormModel,
    product_size_id: int,
    image: Optional[UploadFile] = File(None)
):
    """
    Update a product item size.

    Args:
        current_admin (Admin): The current authenticated admin.
        session (Session): Database session for performing operations.
        product_item_size_detail (ProductItemFormModel): Details of the product item size to be updated.
        product_size_id (int): The ID of the product size to update.
        image (Optional[UploadFile]): Optional new image to upload.

    Raises:
        HTTPException: If the user is not an admin.
        HTTPException: If the product size is not found.
        HTTPException: If an error occurs during the update process.

    Returns:
        ProductItem: The updated product item.
    """
    if not current_admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    product_size = session.exec(select(ProductSize).where(ProductSize.id == product_size_id)).first()
    if not product_size:
        raise HTTPException(status_code=404, detail="Product size not found")

    product_item_id = product_size.product_item_id
    product_item = session.exec(select(ProductItem).where(ProductItem.id == product_item_id)).first()
    if not product_item:
        raise HTTPException(status_code=404, detail="Product item not found")

    try:
        for size_detail in product_item_size_detail.sizes:
            if size_detail.size == product_size.size:
                product_size.price = str(size_detail.price)
                product_size.stock.stock = size_detail.stock

                session.add(product_size)

        if image:
            try:
                product_item.image_url = upload_image(image)
                session.add(product_item)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error occurs during image upload: {e}")

        session.commit()
        session.refresh(product_item)

        return product_item
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error occurs while updating the product size: {e}")
