from ..service.cart_service import create_carts, get_all_carts, update_carts, delete_carts, create_cart_token, get_product_from_token
from ..model.cart import CartItemModel, Cart, CartToken
from ..utils.user_verify import get_current_active_user, get_current_user
from typing import Annotated, Optional, List
from fastapi.responses import ORJSONResponse
from ..model.authentication import Users
from fastapi import APIRouter, Depends, HTTPException
from ..core.db import DB_SESSION
import json

router = APIRouter(prefix="/api/v1/cart")


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


@router.put("/update_cart/{cart_item_id}")
async def update_cart(
                        current_user: Annotated[Users, Depends(get_current_active_user)],
                        session: DB_SESSION,
                        cart_item_id: int,
                        quantity: int,
                    ):

    cart = await update_carts(current_user, session, cart_item_id, quantity)

    return cart


@router.delete("/delete_cart/{cart_item_id}")
async def delete_cart(
                        current_user: Annotated[Users, Depends(get_current_active_user)],
                        session: DB_SESSION,
                        cart_item_id: str
                    ):

    cart = await delete_carts(current_user, session, cart_item_id)

    return cart


@router.post("/create/product_token")
async def create_product_token(
                        # current_user: Annotated[Users, Depends(get_current_active_user)],
                        cart_token_details: CartToken
                    ):
    # cart_token = await create_cart_token(current_user, cart_token_details)
    cart_token = await create_cart_token(cart_token_details)
    return ORJSONResponse({"token": cart_token})


@router.get("/proceed/checkout/{token}")
async def proceed_to_checkout(
    current_user: Annotated[Users, Depends(get_current_active_user)],
    session: DB_SESSION,
    token: str,
    access_token: Optional[bool] = False,
):
    if access_token:
        verify_user = await get_current_user(token, session=session)
        if verify_user.id == current_user.id:
            cart_details = await get_all_carts(current_user, session)
            return cart_details
        else:
            raise HTTPException(status_code=401, detail="Token does not belong to the current user")
    else:
        cart_details = await get_product_from_token(token, session)
        return cart_details