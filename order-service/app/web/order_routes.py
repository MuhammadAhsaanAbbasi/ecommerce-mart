from ..service.order_service import create_orders, get_orders_by_user, get_all_orders, get_orders_by_id, update_orders_status, delete_orders, get_orders_by_status_and_date, cancel_orders_by_customer, get_orders_by_tracking_id
from ..model.order import OrderModel, Order, OrderItem, OrderUpdateStatus
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

order_router = APIRouter(prefix="/api/v1")

# Create Order
@order_router.post("/create_order")
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
                    ):
    orders = await get_orders_by_user(current_user, session)
    return orders

# Get All Orders
@order_router.get("/get_all_orders")
async def get_all_order(
                    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    ):
    orders = await get_all_orders(current_admin, session)
    # order = await get_all_orders(session)
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
@order_router.put("/update_order_status/{order_id}")
async def update_order_status(
                    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    order_id: str,
                    status: str
):
    order_update_details = OrderUpdateStatus(order_id=order_id, status=status)
    order = await update_orders_status(current_admin, session, order_update_details )
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

# Get Order By Status Only Admin
@order_router.get("/get_order_by_status_and_date")
async def get_order_by_status_and_date(
                    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    status: Optional[str] = None,
                    from_date: Optional[datetime] = None,
                    to_date: Optional[datetime] = None
):
    orders = await get_orders_by_status_and_date(current_admin, session, status, from_date, to_date)
    return orders

# Cancel Order By Customer Only User
@order_router.delete("/cancel_order_by_customer")
async def cancel_order_by_customer(
                    current_user: Annotated[Users, Depends(get_current_active_user)],
                    session: DB_SESSION,
                    order_id: str,
):
    order = await cancel_orders_by_customer(current_user, session, order_id)
    return order

#Track Order
@order_router.get("/track_order/{tracking_id}")
async def track_order(
                    session: DB_SESSION,
                    tracking_id: str,
                    ):
    order = await get_orders_by_tracking_id(session, tracking_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order