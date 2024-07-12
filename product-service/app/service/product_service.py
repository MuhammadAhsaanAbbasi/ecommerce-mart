from ..model.models import Product, ProductSize, ProductItem, Stock, ProductFormModel, ProductItemFormModel, SizeModel
from ..product_pb2 import ProductFormModel as ProductFormModelProto, ProductItemFormModel as ProductItemFormModelProto, SizeModel as SizeModelProto # type: ignore
from ..setting import CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, CLOUDINARY_CLOUD, PRODUCT_TOPIC
from ..utils.utils import search_algorithm_by_category, all_product_details
from fastapi import Depends, HTTPException, UploadFile, File, Form
from ..utils.admin_verify import get_current_active_admin_user
from ..model.category_model import Category, Gender, Size
from ..kafka.producer import get_kafka_producer
from ..model.category_model import Category
from ..core.config import upload_files_in_s3
from aiokafka import AIOKafkaProducer # type: ignore
from ..model.authentication import Admin
import cloudinary.uploader # type: ignore
import cloudinary # type: ignore
from typing import Annotated, List
from ..core.db import DB_SESSION
from sqlmodel import select
from sqlalchemy import or_
import json

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
        aio_producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
        session: DB_SESSION,
        product_details: ProductFormModel,
        images: List[UploadFile] = File(...)):
    """
    Create a new product in the database.

    Args:
        images (List[UploadFile]): List of images to be uploaded.
        product_details (ProductFormModel): Details of the product to be created.
        session (Annotated[Session, Depends(get_session)]): Database session for performing operations.
        aio_producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]: AioKafka Implementation Real Time,
        admin_verification (Annotated[Admin, Depends(get_current_active_admin_user)]): Admin verification dictionary obtained via dependency injection.

    Raises:
        HTTPException: If the user is not an admin.
        HTTPException: If the number of images does not match the number of product items.
        HTTPException: If product details are not provided.
        HTTPException: If product Name are also exist.
        HTTPException: If an error occurs during image upload.
        HTTPException: If an error occurs while creating the product.

    Returns:
        Product: The created product.
    """
    if not current_admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    if len(product_details.product_item) != len(images):
        raise HTTPException(status_code=202, detail="The number of images does not match the number of product items")
    
    if not product_details:
        raise HTTPException(status_code=400, detail="Product details not provided")

    available_products = session.exec(select(Product).where(Product.product_name == product_details.product_name)).first()

    if available_products:
        raise HTTPException(status_code=409, detail="Product already exists")

    product_item_tables: List[ProductItem] = []
    try:
        for product_items, image in zip(product_details.product_item, images):
            try:
                image_url = upload_files_in_s3(image)
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

        # Convert product details to protobuf message
        product_proto = ProductFormModelProto(
            product_name=product.product_name,
            product_desc=product.product_desc,
            category_id=int(product.category_id),
            gender_id=int(product.gender_id),
            product_item=[
                ProductItemFormModelProto(
                    color=item.color,
                    image_url=item.image_url,
                    sizes=[
                        SizeModelProto(size=size.size, price=size.price, stock=size.stock.stock)
                        for size in item.sizes
                    ]
                ) for item in product.product_item
            ]
        )

        # Serialize the message to a byte string
        serialized_product = product_proto.SerializeToString()

        # Produce message to Kafka
        await aio_producer.send_and_wait(topic=PRODUCT_TOPIC, value=serialized_product)

        return product
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error Occurs while creating the product: {e}")


# get all product details
async def get_all_product_details(session: DB_SESSION):
    products = session.exec(select(Product)).all()

    product_details = await all_product_details(products, session)

    return product_details


# get specific product details
async def get_specific_product_details(product_id: str, session: DB_SESSION):
    product = session.exec(select(Product).where(Product.product_id == product_id)).first()
    
    if not product:
        return None

    # Fetch category and gender names
    category = session.exec(select(Category).where(Category.id == product.category_id)).first()
    gender = session.exec(select(Gender).where(Gender.id == product.gender_id)).first()

    category_name = category.category_name if category else product.category_id
    gender_name = gender.gender_name if gender else product.gender_id

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
                        size=size.size,
                        price=product_size.price,
                        stock=stock.stock
                    )
                    product_sizes_table.append(size_model)
            
            if product_sizes_table:
                product_item_model = ProductItemFormModel(
                    id=item.id,
                    color=item.color,
                    image_url=item.image_url,
                    sizes=product_sizes_table
                )
                product_items_table.append(product_item_model)

    product_details = ProductFormModel(
            id=product.id,
            product_name=product.product_name,
            product_desc=product.product_desc,
            category_id=category_name,
            gender_id=gender_name,
            product_item=product_items_table
        )

    print(f"product_details: {product_details}")

    return {"data": product_details}



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

    product_details = await all_product_details(unique_products, session)

    return product_details

# get product by category
async def get_product_by_category(catogery:str, session: DB_SESSION):
    category = session.exec(select(Category).where(Category.category_name == catogery)).first()

    if not category:
        raise HTTPException(status_code=404,
                            detail="Category not found")
    
    products = session.exec(select(Product).where(Product.category_id == category.id)).all()

    product_details = await all_product_details(products, session)

    return product_details

# delete product
async def deleted_product(product_id: str,
                        current_admin: Annotated[Admin, Depends(get_current_active_admin_user)], 
                        session: DB_SESSION):
    if not current_admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    product = session.exec(select(Product).where(Product.product_id == product_id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Retrieve all product items related to the product
    product_items = session.exec(select(ProductItem).where(ProductItem.product_id == product_id)).all()
    
    for item in product_items:
        # Retrieve all product sizes related to the product item
        product_sizes = session.exec(select(ProductSize).where(ProductSize.product_item_id == item.id)).all()
        
        for size in product_sizes:
            # Retrieve and delete the stock related to the product size
            stock = session.exec(select(Stock).where(Stock.product_size_id == size.id)).first()
            if stock:
                session.delete(stock)
        
            # Delete the product size
            session.delete(size)
        
        # Delete the product item
        session.delete(item)
    
    # Finally, delete the product
    session.delete(product)
    session.commit()

    return {"data": f"Product with ID {product_id} and all its related items have been deleted"}