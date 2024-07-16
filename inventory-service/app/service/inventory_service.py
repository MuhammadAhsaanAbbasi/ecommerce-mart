from ..model.models import Product, ProductSize, ProductItem, ProductItemFormModel, SizeModel, Stock, Size
from ..inventory_pb2 import ProductItemFormProtoModel as ProductItemFormModelProto, SizeProtoModel as SizeModelProto # type: ignore
from fastapi import Depends, UploadFile, File, HTTPException
from ..utils.admin_verify import get_current_active_admin_user
from ..kafka.producer import get_kafka_producer, AIOKafkaProducer
from ..utils.auth import upload_image
from typing import Annotated, List
from ..model.authentication import Admin
from ..core.db import DB_SESSION
from sqlmodel import select
# from app import inventory_pb2
from app.setting import INVENTORY_TOPIC


# Product Item
async def create_product_item(
    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
    aio_kafka: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
    session: DB_SESSION,
    product_id: str,
    product_item_detail: ProductItemFormModel,
    image: UploadFile = File(...),
):
    """
    Create a new product item in the database.

    Args:
        current_admin (Admin): The current authenticated admin.
        aio_kafka (AIOKafkaProducer): Kafka producer instance.
        session (Session): Database session for performing operations.
        product_id (int): ID of the product to which the item belongs.
        product_item_detail (ProductItemFormModel): Details of the product item to be created.
        image (UploadFile): The image to be uploaded for the product item.

    Raises:
        HTTPException: If the user is not an admin.
        HTTPException: If the product is not found.
        HTTPException: If an error occurs during image upload.
        HTTPException: If an error occurs while creating the product item.

    Returns:
        ProductItem: The created product item.
    """
    if not current_admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    product = session.exec(select(Product).where(Product.product_id == product_id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    try:
        image_url = await upload_image(image)

        product_size_tables: List[ProductSize] = []
        for product_size in product_item_detail.sizes:
            stock_tables = Stock(stock=product_size.stock)
            product_size_schema = ProductSize(size=product_size.size, price=product_size.price, stock=stock_tables)
            product_size_tables.append(product_size_schema)

        product_item = ProductItem(
            color=product_item_detail.color,
            image_url=image_url,
            sizes=product_size_tables,
            product_id=product.id
        )

        session.add(product_item)
        session.commit()
        session.refresh(product_item)

        # Convert product item details to protobuf message
        product_item_proto = ProductItemFormModelProto(
            product_id=product_id,
            color=product_item.color if product_item.color else "",
            image_url=product_item.image_url if product_item.image_url else "",
            sizes=[
                SizeModelProto(size=size.size, price=size.price, stock=size.stock.stock)
                for size in product_item.sizes
            ]
        )

        # Serialize the message to a byte string
        serialized_product_item = product_item_proto.SerializeToString()

        # Produce message to Kafka
        await aio_kafka.send_and_wait(topic=INVENTORY_TOPIC, value=serialized_product_item)

        return product_item
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error Occurs while creating the product item: {e}")

async def get_product_item(
                    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    product_id: str):
    
    if not current_admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    product = session.exec(select(Product).where(Product.product_id == product_id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product_items = session.exec(select(ProductItem).where(ProductItem.product_id == product.id)).all()
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

async def delete_product_item(
                    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
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

async def update_product_item_image(
    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
    session: DB_SESSION,
    product_item_id: int,
    image: UploadFile = File(...)
):
    """
    Update the image URL of a product item.

    Args:
        current_admin (Admin): The current active admin user.
        session (DB_SESSION): The database session for performing operations.
        product_item_id (int): The ID of the product item to be updated.
        image (UploadFile): The new image to be uploaded for the product item.

    Returns:
        ProductItem: The updated product item.
    """
    if not current_admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    product_item = session.exec(select(ProductItem).where(ProductItem.id == product_item_id)).first()
    if not product_item:
        raise HTTPException(status_code=404, detail="Product item not found")

    try:
        image_url = await upload_image(image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurs during image upload: {e}")

    # Update the image URL of the product item
    product_item.image_url = image_url

    # Commit the changes to the database
    # session.add(product_item)
    session.commit()
    # session.refresh(product_item)

    return {"message": "Product Item Image Updated Successfully!"}