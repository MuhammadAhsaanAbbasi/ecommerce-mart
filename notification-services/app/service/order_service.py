from ..model.order import OrderModel, OrderDetails, OrderItemDetails
from ..core.config import send_email_via_ses
from ..model.models import Product, ProductItem, ProductSize, Size, Color
from fastapi import HTTPException
from ..core.db import DB_SESSION
from sqlmodel import select
from typing import List

async def send_order_confirmation_email(order: OrderModel, session: DB_SESSION):
    order_item_details: List[OrderItemDetails] = []
    for item in order.items:
        product = session.exec(select(Product).where(Product.id == item.product_id)).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        product_item = session.exec(select(ProductItem)
                                    .where(ProductItem.product_id == product.id)
                                    .where(ProductItem.id == item.product_item_id)).first()
        if not product_item:
            raise HTTPException(status_code=404, detail="Product item not found")
        
        color = session.exec(select(Color).where(Color.id == product_item.color)).first()
        if not color:
            raise HTTPException(status_code=404, detail="Color not found")
        
        product_size = session.exec(select(ProductSize)
                                    .where(ProductSize.product_item_id == product_item.id)
                                    .where(ProductSize.id == item.product_size_id)).first()
        if not product_size:
            raise HTTPException(status_code=404, detail="Product size not found")
        
        size = session.exec(select(Size).where(Size.id == product_size.size)).first()
        if not size:
            raise HTTPException(status_code=404, detail="Size not found")
        
        item_price = product_size.price * item.quantity

        order_item_details.append(OrderItemDetails(
            product_name=product.product_item,
            product_image_url=product_item.image_url,
            product_color=color.color_name,
            product_size=size.size,
            quantity=item.quantity,
            price=item_price
        ))
    
    # order_details = OrderDetails(
    #     order_id=order.id,
    #     email=order.email,
    #     country=order.country,
    #     city=order.city,
    #     postal_code=order.postal_code,
    #     address=order.address,
    #     phone_number=order.phone_number,
    #     total_price=order.total_price,
    #     order_payment=order.order_payment,
    #     order_items=order_item_details
    # )
    
    # order_details = OrderDetails