from ..model.product import Product, ProductItem, ProductSize, Stock, SizeModel, ProductItemFormModel, ProductFormModel
from ..model.order import OrderModel, Order, OrderItem, OrderUpdateStatus 
from ..utils.actions import create_order
from fastapi import Depends, UploadFile, File, Form, HTTPException
from ..utils.admin_verify import get_current_active_admin_user
from ..utils.user_verify import get_current_active_user
from ..model.authentication import Users, Admin
from typing import Annotated, Optional, List
from ..core.db import DB_SESSION
from sqlmodel import select
import json


async def create_orders(
                    order_details: OrderModel,
                    session: DB_SESSION, 
                    current_user: Annotated[Users, Depends(get_current_active_user)],
                    ):
    
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user.id is None:
        raise HTTPException(status_code=400, detail="User ID is invalid")

    if order_details.order_payment != "Online Payment":
        order = await create_order(order_details, current_user.id, session)
        return order
    else:
        return {'message': "Order Created Successfully! & Charged Online Payment!"}


async def get_orders_by_user(
                    current_user: Annotated[Users, Depends(get_current_active_user)],
                    session: DB_SESSION,
                    ):
    return {'message' : "Order Created Successfully!"}


async def get_all_orders(
                    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    ):
    return {'message' : "Order Created Successfully!"}


async def get_orders_by_id(
                    session: DB_SESSION,
                    order_id: int,
                    ):
    return {'message' : "Order Created Successfully!"}


async def update_orders_status(
                    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    order_id: int,
                    ):
    return {'message' : "Order Created Successfully!"}


async def delete_orders(
                    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    order_id: int,
                    ):
    return {'message' : "Order Created Successfully!"}


async def get_orders_by_status(
                    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    status: str,
                    ):
    return {'message' : "Order Created Successfully!"}


async def cancel_orders_by_customer(
                    current_user: Annotated[Users, Depends(get_current_active_user)],
                    session: DB_SESSION,
                    order_id: int,
                    ):
    return {'message' : "Order Created Successfully!"}