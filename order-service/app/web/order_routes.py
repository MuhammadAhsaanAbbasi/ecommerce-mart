from ..model.order import OrderModel, Order, OrderItem, Product, ProductItem, ProductSize, Stock
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from ..utils.admin_verify import get_current_active_admin_user
from ..utils.user_verify import get_current_active_user
from ..model.authentication import Users, Admin
from typing import Annotated, Optional, List
from ..core.db import DB_SESSION
from sqlmodel import Session
import json

order_router = APIRouter(prefix="/api/v1")

@order_router.get("/create-order")
async def create_order(
                    current_user: Annotated[Users, get_current_active_user],
                    session: DB_SESSION,
                    
                    ):
    return {"message" : "Order Services"}