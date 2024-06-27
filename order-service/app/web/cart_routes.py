from ..service.cart_service import create_carts, get_all_carts, update_carts, delete_carts
from ..model.cart import CartItemModel, Cart, CartItem, CartUpdateItem
from ..utils.user_verify import get_current_active_user
from typing import Annotated, Optional, List
from ..model.authentication import Users
from fastapi import APIRouter, Depends
from ..core.db import DB_SESSION
import json

router = APIRouter(prefix="/api/v1")


@router.post("/create-cart")
async def create_cart(
                        current_user: Annotated[Users, Depends(get_current_active_user)],
                        session: DB_SESSION,
                        cart_details: CartItemModel
                    ):
    
    cart = await create_carts(current_user, session, cart_details)
    
    return cart


@router.get("/get_all_carts")
async def get_all_cart(
                        current_user: Annotated[Users, Depends(get_current_active_user)],
                        session: DB_SESSION,
                        ):

    carts = await get_all_carts(current_user, session)

    return carts


@router.put("/update_cart")
async def update_cart(
                        current_user: Annotated[Users, Depends(get_current_active_user)],
                        session: DB_SESSION,
                        cart_details: CartUpdateItem
                    ):

    cart = await update_carts(current_user, session, cart_details)

    return cart


@router.delete("/delete_cart")
async def delete_cart(
                        current_user: Annotated[Users, Depends(get_current_active_user)],
                        session: DB_SESSION,
                        cart_item_id: int
                    ):

    cart = await delete_carts(current_user, session, cart_item_id)

    return cart