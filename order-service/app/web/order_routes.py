from ..service.order_service import create_orders, get_orders_by_user, get_orders_by_id, update_orders_status, delete_orders, fetch_orders, cancel_orders_by_customer, get_user_orders_by_status
from ..model.order import OrderModel, Order, OrderItem, OrderStatus
from ..kafka.producer import AIOKafkaProducer, get_kafka_producer
from ..utils.admin_verify import get_current_active_admin_user
from ..utils.user_verify import get_current_active_user
from fastapi import APIRouter, Depends, HTTPException
from ..model.authentication import Users, Admin
from typing import Annotated, Optional, List
from ..core.db import DB_SESSION
from datetime import datetime
from sqlmodel import Session
import json

order_router = APIRouter(prefix="/api/v1/order")

# Create Order
@order_router.post("/create")
async def create_order(
                    session: DB_SESSION,
                    order_details: OrderModel,
                    current_user: Annotated[Users, Depends(get_current_active_user)],
                    aio_producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
                    ):
    order = await create_orders(order_details, session, current_user, aio_producer)
    return order

# Get Order By User 
@order_router.get("/get_order_by_user")
async def get_order_by_user(
        current_user: Annotated[Users, Depends(get_current_active_user)],
        session: DB_SESSION,
        page: int = 1, 
        limit: int = 5, 
    ):
    offset = (page - 1) * limit
    orders = await get_orders_by_user(current_user, session, limit, offset)
    return orders

# Get All Orders
@order_router.get("/get_all_orders")
async def get_all_orders(
        # current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
        session: DB_SESSION,
        page: int = 1, 
        limit: int = 5, 
        status: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ):
    offset = (page - 1) * limit
    # orders = await fetch_orders(current_admin, session, limit, offset, status, from_date, to_date)
    orders = await fetch_orders(session, limit, offset, status, from_date, to_date)
    return orders

# Get Order Details by Id
@order_router.get("/get_order_by_id/{order_id}")
async def get_order_by_id(
                    session: DB_SESSION,
                    order_id: str,
                    ):
    order = await get_orders_by_id(session, order_id)
    return order

# Update Order Status
@order_router.put("/update/order_status/{order_id}")
async def update_order_status(
                    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    order_id: str,
                    order_status: OrderStatus
):
    order = await update_orders_status(current_admin, session, order_id, order_status )
    return order

# Delete Order By Admin
@order_router.delete("/delete_order/{order_id}")
async def delete_order(
                    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    order_id: str,
):
    order = await delete_orders(current_admin, session, order_id)
    return order

# Cancel Order By Customer Only User
@order_router.delete("/cancel_order_by_customer/{order_id}")
async def cancel_order_by_customer(
                    current_user: Annotated[Users, Depends(get_current_active_user)],
                    session: DB_SESSION,
                    order_id: str,
):
    order = await cancel_orders_by_customer(current_user, session, order_id)
    return order

# User Orders on the Base of Order Status
@order_router.get('/user_orders/{status}')
async def user_orders(
                    current_user: Annotated[Users, Depends(get_current_active_user)],
                    session: DB_SESSION,
                    status: str,
                    page: int = 1,
                    limit: int = 10,
                    ):
    offset = (page - 1) * limit
    user_orders = await get_user_orders_by_status(current_user, session, status, offset, limit,)
    return user_orders