from ..model.models import ProductSize, ProductItem, ProductItemFormModel, SizeModel, Stock, Size
from ..utils.admin_verify import get_current_active_admin_user
from fastapi import Depends, HTTPException
from ..core.db import DB_SESSION
from ..model.authentication import Admin
from typing import Annotated
from sqlmodel import select

# Product Sizes
async def create_product_size(
    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
    session: DB_SESSION,
    product_size_detail: SizeModel,
    product_item_id: str
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
            product_item_id=product_item.id
        )

        session.add(product_size)
        session.commit()
        session.refresh(product_size)

        return product_size
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error Occurs while creating the product size: {e}")

async def delete_product_size(
    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
    session: DB_SESSION,
    product_size_id: str
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