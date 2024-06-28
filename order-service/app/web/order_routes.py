from ..service.order_service import create_orders, get_orders_by_user, get_all_orders, get_orders_by_id, update_orders_status, delete_orders, get_orders_by_status, cancel_orders_by_customer
from ..model.order import OrderModel, Order, OrderItem
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from ..utils.admin_verify import get_current_active_admin_user
from ..utils.user_verify import get_current_active_user
from ..model.authentication import Users, Admin
from typing import Annotated, Optional, List
from ..core.db import DB_SESSION
from sqlmodel import Session
import json

order_router = APIRouter(prefix="/api/v1")

# Create Order
@order_router.post("/create_order")
async def create_order(
                    order_details: OrderModel,
                    session: DB_SESSION, 
                    current_user: Annotated[Users, Depends(get_current_active_user)],
                    ):
    order = await create_orders(order_details, session, current_user)
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
                    order_id: int,
                    ):
    order = await get_orders_by_id(session, order_id)
    return order

# Update Order Status
@order_router.put("/update_order_status/{order_id}")
async def update_order_status(
                    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    order_id: int,
):
    order = await update_orders_status(current_admin, session, order_id )
    return order

# Delete Order By Admin
@order_router.delete("/delete_order/{order_id}")
async def delete_order(
                    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    order_id: int,
):
    order = await delete_orders(current_admin, session, order_id)
    return order

# Get Order By Status Only Admin
@order_router.get("/get_order_by_status")
async def get_order_by_status(
                    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    status: str,
):
    orders = await get_orders_by_status(current_admin, session, status)
    return orders

# Cancel Order By Customer Only User
@order_router.delete("/cancel_order_by_customer")
async def cancel_order_by_customer(
                    current_user: Annotated[Users, Depends(get_current_active_user)],
                    session: DB_SESSION,
                    order_id: int,
):
    order = await cancel_orders_by_customer(current_user, session, order_id)
    return order