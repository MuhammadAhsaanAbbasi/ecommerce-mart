from ..model.order import Product, ProductItem, ProductSize, Stock
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from ..utils.user_verify import get_current_active_user
from ..model.authentication import Users
from ..model.cart import CartItemModel, Cart, CartItem, CartUpdateItem
from typing import Annotated, Optional, List
from ..core.db import DB_SESSION
import json


async def create_carts(
                        current_user: Annotated[Users, get_current_active_user],
                        session: DB_SESSION,
                        cart_details: CartItemModel
                    ):
    """
    summary: 
    User Have to Choice to add Products in a Cart

    Args:
        current_user (Annotated[Users, get_current_active_user]): _description_
        session (DB_SESSION): _description_
        cart_details (CartItemModel): _description_

    Returns:
        Cart: The Cart Created OR Updated.
    """

    return {"message" : "Cart has been Created Successfully!"}

async def get_all_carts(
                        current_user: Annotated[Users, get_current_active_user],
                        session: DB_SESSION,
                        ):
    return {"message" : "Get all carts of User"}

async def update_carts(
                        current_user: Annotated[Users, get_current_active_user],
                        session: DB_SESSION,
                        cart_details: CartUpdateItem
                    ):
    return {"message" : "Cart has been Updated Successfully!"}

async def delete_carts(
                        current_user: Annotated[Users, get_current_active_user],
                        session: DB_SESSION,
                        cart_item_id: int
                    ):
    return {"message" : "Cart has been Deleted Successfully!"}
