from ..service.cart_service import create_carts, get_all_carts, update_carts, delete_carts
from ..model.cart import CartItemModel, Cart, CartItem, CartUpdateItem
from ..utils.user_verify import get_current_active_user
from ..model.authentication import Users
from typing import Annotated, Optional, List
from ..core.db import DB_SESSION
from fastapi import APIRouter
import json

router = APIRouter(prefix="/api/v1")

@router.get("/create-cart")
async def create_cart(
                        current_user: Annotated[Users, get_current_active_user],
                        session: DB_SESSION,
                        cart_details: CartItemModel
                    ):
    
    cart = await create_carts(current_user, session, cart_details)
    
    return {"message" : "Order Services"}


@router.get("/get_all_carts")
async def get_all_cart(
                        current_user: Annotated[Users, get_current_active_user],
                        session: DB_SESSION,
                        ):

    cart = await get_all_carts(current_user, session)

    return {"message" : "Order Services"}


@router.put("/update_cart")
async def update_cart(
                        current_user: Annotated[Users, get_current_active_user],
                        session: DB_SESSION,
                        cart_details: CartUpdateItem
                    ):

    cart = await update_carts(current_user, session, cart_details)

    return {"message" : "Order Services"}


@router.delete("/delete_cart")
async def delete_cart(
                        current_user: Annotated[Users, get_current_active_user],
                        session: DB_SESSION,
                        cart_item_id: int
                    ):

    cart = await delete_carts(current_user, session, cart_item_id)

    return {"message" : "Order Services"}