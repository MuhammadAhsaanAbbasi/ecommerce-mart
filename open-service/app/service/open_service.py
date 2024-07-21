from ..model.product import Product, ProductItem, ProductSize, Stock, SizeModel, ProductItemFormModel, ProductFormModel, Size
from ..model.order import OrderModel, Order, OrderItem, OrderUpdateStatus, OrderItemDetail, OrderDetail, OrderStatus
from ..utils.admin_verify import get_current_active_admin_user
from ..utils.actions import all_product_details
from ..utils.user_verify import get_current_active_user
from fastapi import Depends, HTTPException, Query
from ..model.authentication import Users, Admin
from typing import Annotated, Optional, List, Sequence
from ..core.db import DB_SESSION
from datetime import datetime, timedelta
from sqlmodel import select
import json
import uuid

async def get_all_product_details(session: DB_SESSION):
    products = session.exec(select(Product)).all()

    product_details = await all_product_details(products, session)

    return product_details

async def get_features_product(session: DB_SESSION):
    # Get all features Product which create 14 days ago from now
    current_date = datetime.now()
    two_weeks_ago = current_date - timedelta(days=14)
    
    if not Product.created_at:
        raise HTTPException(status_code=400, detail="Products date not found")
    products = session.exec(select(Product).where(Product.created_at >= two_weeks_ago)).all()

    product_details = await all_product_details(products, session)
    return product_details

# Get Order By Id
async def get_orders_by_tracking_id(
                    session: DB_SESSION,
                    tracking_id: str,
                    ):
    order = session.exec(select(Order).where(Order.tracking_id == tracking_id)).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    try:
        order_items = session.exec(select(OrderItem).where(OrderItem.order_id == order.id)).all()
        order_items_detail = []

        for order_item in order_items:
            product = session.exec(select(Product).where(Product.id == order_item.product_id)).first()
            product_item = session.exec(select(ProductItem).where(ProductItem.id == order_item.product_item_id)).first()
            product_size = session.exec(select(ProductSize).where(ProductSize.id == order_item.product_size_id)).first()
            stock = session.exec(select(Stock).where(Stock.product_size_id == order_item.product_size_id)).first()

            if product and product_item and product_size and stock:
                size = session.exec(select(Size).where(Size.id == product_size.size)).first()
                if not size:
                    raise HTTPException(status_code=404, detail="Size not found")

                order_item_detail = OrderItemDetail(
                    product=product.product_name,
                    product_item={
                        'color': product_item.color,
                        'image_url': product_item.image_url
                    },
                    size=size.size,
                    price=product_size.price,
                    quantity=order_item.quantity,
                    stock=stock.stock,
                )
                order_items_detail.append(order_item_detail)

        order_detail = OrderDetail(
                order_id=order.id,
                order_address=order.order_address,
                phone_number=order.phone_number,
                order_payment=order.order_payment,
                total_price=order.total_price,
                order_status=order.order_status,
                tracking_id=order.tracking_id,
                delivery_date=order.delivery_date,
                order_date=order.order_date,
                order_items=order_items_detail
            )

        return order_detail
    except HTTPException as e:
        raise e