from ..service.inventory_service import create_product_item, get_product_item_details, delete_product_item, update_product_item
from ..service.product_size import create_product_size, delete_product_size
from ..model.models import ProductItemFormModel, SizeModel, Stock, ProductItemUpdateModel
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from ..kafka.producer import get_kafka_producer, AIOKafkaProducer
from ..utils.admin_verify import get_current_active_admin_user
from typing import Annotated, Optional
from ..core.db import DB_SESSION
from ..model.authentication import Admin
import json

router = APIRouter(prefix="/api/v1/inventory")

# Product Item Routes
@router.post("/create/product_item")
async def create_product_items(
    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
    aio_kafka: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
    session: DB_SESSION,
    product_id: str,
    product_item_details: Annotated[str, Form(...)],
    image: UploadFile = File(...),
):
    """
    Create a new product item in the database.

    Args:
        product_item_details: Annotated[str, Form(...)] = {
        "color": "string", 
        "product_id": int,
        "sizes": [ { "size": int, "price": int, "stock": int } ] 
        }
    """
    try:
        product_item_details_dict = json.loads(product_item_details)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data provided for product item details")

    product_item_details_model = ProductItemFormModel(**product_item_details_dict)
    product_item = await create_product_item(current_admin, aio_kafka, session, product_id, product_item_details_model, image)
    # product_item = await create_product_item(aio_kafka, session, product_id, product_item_details_model, image)
    return {"message": "Create Product Item Successfully!", "data": product_item}

@router.get("/product_item")
async def get_product_items_details(
                    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    product_item_id: str):
    product_items = await get_product_item_details(current_admin, session, product_item_id)
    # product_items = await get_product_item_details(session, product_item_id)
    return {"message" : "Item of Product Get Successfully!", "data" : product_items}

@router.delete("/product_item")
async def delete_product_items(
                    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    product_item_id: str):
    product_item = await delete_product_item(current_admin, session, product_item_id)
    # product_item = await delete_product_item(session, product_item_id)
    return {"message" : "Item of Product Delete Successfully!", "data" : product_item}

# Product Size 
@router.post("/product_size")
async def create_product_sizes(
                        current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        session: DB_SESSION,
                        product_size_detail: SizeModel,
                        product_item_id: str
                        ):
    product_size = await create_product_size(current_admin, session, product_size_detail, product_item_id)
    # product_size = await create_product_size(session, product_size_detail, product_item_id)
    return {"message" : "Size of Product Create Successfully!", "data" : product_size }

@router.delete("/product_size")
async def delete_product_sizes(
                        current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        session: DB_SESSION,
                        product_size_id: str):
    product_size = await delete_product_size(current_admin, session, product_size_id)
    # product_size = await delete_product_size(session, product_size_id)
    return {"message" : "Size of Product Delete Successfully!", "data" : product_size}


# Update Product Item & Size
@router.put("/update/product_item_size/{product_item_id}")
async def update_product_item_route(
    product_item_id: str,
    product_item_input: Annotated[str, Form(...)],
    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
    session: DB_SESSION,
    image: Optional[UploadFile] = None
):
    """
    Update the image URL of an existing product item.

    Args:
        product_item_input : Annotated[str, Form(...)] = {
            "color": "string",
            "sizes": [
    {
        "size": "size id",
        "price": 0,
        "stock": 0
        }
    ]
}

    Returns:
        dict: A success message and updated product item data.
    """
    try: 
        product_item_details_dict = json.loads(product_item_input)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data provided for product details")

    product_item_details_model = ProductItemUpdateModel(**product_item_details_dict)
    product_item = await update_product_item(product_item_id, product_item_details_model, current_admin, session, image)
    # product_item = await update_product_item(product_item_id, product_item_details_model, session, image)
    return product_item 
