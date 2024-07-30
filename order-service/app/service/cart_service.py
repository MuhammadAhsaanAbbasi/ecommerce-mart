from ..model.product import Color, Product, ProductItem, ProductSize, Stock, Size, ProductItemFormModel, ProductFormModel, SizeModelDetails, ProductItemDetails, ProductDetails
from fastapi import Depends, UploadFile, File, Form, HTTPException, status
from ..model.cart import CartItemModel, Cart, CartItem, CartToken, CartDetails, CartItemDetail
from ..utils.user_verify import get_current_active_user
from ..model.authentication import Users
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional, List
from ..setting import SECRET_KEY, ALGORITHM
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
    cart_item_total_price_details = []

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
        size = session.exec(select(Size).where(Size.id == product_size.size)).first()

        size_model = SizeModelDetails(
            product_size_id=product_size.id,
            size=size.size if size else "",
            price=product_size.price,
            stock=stock.stock if stock else 0
        )

        color = session.exec(select(Color).where(Color.id == product_item.color)).first()

        product_item_model = ProductItemDetails(
            product_item_id=product_item.id,
            color=product_item.color,
            color_name=color.color_name if color else "None",
            color_value=color.color_value if color else "None",
            image_url=product_item.image_url,
            sizes=[size_model]
        )

        product_details = ProductDetails(
            product_id=product.id,
            product_name=product.product_name,
            product_desc=product.product_desc,
            featured=product.featured,
            category_id=product.category_id,
            product_item=[product_item_model]
        )

        cart_item_total_price = cart_item.quantity * product_size.price
        cart_item_total_price_details.append(cart_item_total_price)

        cart_item_detail = {
            "cart_item_id": cart_item.id,
            "quantity": cart_item.quantity,
            "cart_item_total_price": cart_item_total_price,
            "product_details": product_details
        }

        cart_items_details.append(cart_item_detail)

    total_price = sum(cart_item_total_price_details)
    cart_details = {
        "cart_items": cart_items_details,
        "total_price": total_price,
    }

    return cart_details

async def update_carts(
    current_user: Annotated[Users, Depends(get_current_active_user)],
    session: DB_SESSION,
    cart_item_id: int,
    quantity: int,
    
):
    """
    summary:
    User can update the quantity of items in the cart

    Args:
        current_user (Annotated[Users, get_current_active_user]): The current active user
        session (Session): Database session
        cart_details (CartUpdateItem): Details of the cart item to update

    Returns:
        dict: Message indicating the result of the operation
    """

    user_cart = session.exec(select(Cart).where(Cart.user_id == current_user.id)).first()
    if not user_cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    # Initialize a flag to check if the cart item is found
    cart_item_found = False

    for cart_item in user_cart.cart_items:
        if cart_item.id == cart_item_id:
            cart_item.quantity = quantity
            cart_item_found = True
            session.commit()
            break

    if not cart_item_found:
        raise HTTPException(status_code=404, detail="Cart item not found")

    return {"message": "Cart has been updated successfully!"}


async def delete_carts(
    current_user: Annotated[Users, Depends(get_current_active_user)],
    session: DB_SESSION,
    cart_item_id: str
):
    """
    summary:
    User can delete items from the cart

    Args:
        current_user (Annotated[Users, get_current_active_user]): The current active user
        session (Session): Database session
        cart_item_id (int): ID of the cart item to delete

    Returns:
        dict: Message indicating the result of the operation
    """
    
    user_cart = session.exec(select(Cart).where(Cart.user_id == current_user.id)).first()
    if not user_cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    # Check if the cart item exists
    cart_item_found = False

    for cart_item in user_cart.cart_items:
        if cart_item.id == cart_item_id:
            session.delete(cart_item)
            cart_item_found = True
            session.commit()
            break

    if not cart_item_found:
        raise HTTPException(status_code=404, detail="Cart item not found")

    return {"message": "Cart item has been deleted successfully!"}

async def create_cart_token(
                        # current_user: Annotated[Users, Depends(get_current_active_user)],
                        cart_token_details: CartToken
                    ):
    """
                        summary:
                        User can create a cart token

                        Args:
                            current_user (Annotated[Users, get_current_active_user]): The current active user
                            session (Session): Database session
                            cart_token_details (CartToken): Details of the cart token to create

                        Returns:
                            dict: Message indicating the result of the operation
    """
    # if not current_user:
    #     raise HTTPException(status_code=401, detail="Unauthorized")

    if not isinstance(SECRET_KEY, str):
        raise ValueError("SECRET_KEY must be a string")
    if not isinstance(ALGORITHM, str):
        raise ValueError("ALGORITHM must be a string")
    
    expire = datetime.now(timezone.utc) + timedelta(hours=25)
    
    payload = {
        "product_details": cart_token_details.model_dump(),  # Serialize CartToken to dictionary
        "exp": expire
    }

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_product_from_token(token: str, session: DB_SESSION):
    """
                        summary:
                        User can get products from a cart token

                        Args:
                            token (str): The cart token
                            session (Session): Database session

                        Returns:
                            dict: Details of the products in the cart
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        product_details = payload.get("product_details")
        if product_details is None or not isinstance(product_details, dict):
            raise HTTPException(status_code=401, detail="Invalid token details")
        cart_token = CartToken(**product_details)
        try:
            # Create the response in the same format as get_all_carts
            product = session.exec(select(Product).where(Product.id == cart_token.product_id)).first()
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")

            product_item = session.exec(select(ProductItem).where(ProductItem.id == cart_token.product_item_id)).first()
            if not product_item:
                raise HTTPException(status_code=404, detail="Product item not found")

            product_size = session.exec(select(ProductSize).where(ProductSize.id == cart_token.product_size_id)).first()
            if not product_size:
                raise HTTPException(status_code=404, detail="Product size not found")

            stock = session.exec(select(Stock).where(Stock.product_size_id == product_size.id)).first()
            size = session.exec(select(Size).where(Size.id == product_size.size)).first()

            size_model = SizeModelDetails(
                    product_size_id=product_size.id,
                    size=size.size if size else "",
                    price=product_size.price,
                    stock=stock.stock if stock else 0
                )

            color = session.exec(select(Color).where(Color.id == product_item.color)).first()

            product_item_model = ProductItemDetails(
                    product_item_id=product_item.id,
                    color=product_item.color,
                    color_name=color.color_name if color else "None",
                    color_value=color.color_value if color else "None",
                    image_url=product_item.image_url,
                    sizes=[size_model]
                )

            product_details = ProductDetails(
                    product_id=product.id,
                    product_name=product.product_name,
                    product_desc=product.product_desc,
                    featured=product.featured,
                    category_id=product.category_id,
                    product_item=[product_item_model]
                )

            cart_item_total_price = cart_token.quantity * product_size.price

            cart_item_detail = CartItemDetail(
                    cart_item_id=cart_token.product_id,
                    quantity=cart_token.quantity,
                    cart_item_total_price=cart_item_total_price,
                    product_details=product_details
                )
            cart_details = CartDetails(
                    cart_items=[cart_item_detail],
                    total_price=cart_item_total_price
                )

            return cart_details.model_dump()
        except HTTPException as e:
            raise e
    except JWTError:
        raise credentials_exception