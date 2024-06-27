from ..model.product import Product, ProductItem, ProductSize, Stock, SizeModel, ProductItemFormModel, ProductFormModel
from fastapi import Depends, UploadFile, File, Form, HTTPException
from ..utils.user_verify import get_current_active_user
from ..model.authentication import Users
from ..model.cart import CartItemModel, Cart, CartItem, CartUpdateItem
from typing import Annotated, Optional, List
from ..core.db import DB_SESSION
from sqlmodel import select
import json

async def create_carts(
    current_user: Annotated[Users, Depends(get_current_active_user)],
    session: DB_SESSION,
    cart_details: CartItemModel
):
    """
    summary: 
    User has the choice to add products to a cart

    Args:
        current_user (Annotated[Users, get_current_active_user]): The current active user
        session (Session): Database session
        cart_details (CartItemModel): Details of the cart item to add

    Returns:
        dict: Message indicating the result of the operation
    """

    # Check if the user has an existing cart
    user_cart = session.exec(select(Cart).where(Cart.user_id == current_user.id)).first()

    if user_cart:
        # User has a cart, check for the item in the cart
        user_cart_items = user_cart.cart_items
        for item in user_cart_items:
            if item.product_item_id == cart_details.product_item_id and item.product_size_id == cart_details.product_size_id:
                # Item exists in the cart, update the quantity of items
                item.quantity += cart_details.quantity
                session.commit()
                return {"message": "Cart has been updated successfully!"}

        # Item does not exist, add new item to the cart
        new_cart_item = CartItem(
            product_item_id=cart_details.product_item_id,
            product_size_id=cart_details.product_size_id,
            quantity=cart_details.quantity,
            cart_id=user_cart.id
        )
        session.add(new_cart_item)
        session.commit()
        return {"message": "Item has been added to the cart successfully!"}
    else:
        # User does not have a cart, create a new cart and add the item
        new_cart_item = CartItem(
            product_item_id=cart_details.product_item_id,
            product_size_id=cart_details.product_size_id,
            quantity=cart_details.quantity,
        )
        new_cart = Cart(
            user_id=current_user.id,
            cart_items=[new_cart_item]
            )
        
        session.add(new_cart)
        session.commit()

        return {"message": "Cart has been created and item has been added successfully!"}


async def get_all_carts(
    current_user: Annotated[Users, Depends(get_current_active_user)],
    session: DB_SESSION,
):
    user_cart = session.exec(select(Cart).where(Cart.user_id == current_user.id)).first()

    if not user_cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_items_details = []
    for cart_item in user_cart.cart_items:
        product_item = session.exec(select(ProductItem).where(ProductItem.id == cart_item.product_item_id)).first()

        if not product_item:
            raise HTTPException(status_code=404, detail="Product item not found")
        
        product = session.exec(select(Product).where(Product.id == product_item.product_id)).first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        product_size = session.exec(select(ProductSize).where(ProductSize.id == cart_item.product_size_id)).first()

        if not product_size:
            raise HTTPException(status_code=404, detail="Product size not found")

        stock = session.exec(select(Stock).where(Stock.product_size_id == product_size.id)).first()

        size_model = SizeModel(
            id=product_size.id,
            size=product_size.size,
            price=product_size.price,
            stock=stock.stock if stock else 0
        )

        product_item_model = ProductItemFormModel(
            id=product_item.id,
            color=product_item.color,
            image_url=product_item.image_url,
            sizes=[size_model]
        )

        product_details = ProductFormModel(
            id=product.id,
            product_name=product.product_name,
            product_desc=product.product_desc,
            category_id=product.category_id,
            gender_id=product.gender_id,
            product_item=[product_item_model]
        )

        cart_item_detail = {
            "cart_item_id": cart_item.id,
            "quantity": cart_item.quantity,
            "product_details": product_details
        }

        cart_items_details.append(cart_item_detail)

    return {"data": cart_items_details}

async def update_carts(
                        current_user: Annotated[Users, Depends(get_current_active_user)],
                        session: DB_SESSION,
                        cart_details: CartUpdateItem
                    ):
    return {"message" : "Cart has been Updated Successfully!"}

async def delete_carts(
                        current_user: Annotated[Users, Depends(get_current_active_user)],
                        session: DB_SESSION,
                        cart_item_id: int
                    ):
    return {"message" : "Cart has been Deleted Successfully!"}
