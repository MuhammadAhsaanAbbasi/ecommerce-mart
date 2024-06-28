from ..model.product import Product, ProductItem, ProductSize, Stock, SizeModel, ProductItemFormModel, ProductFormModel
from ..model.order import OrderModel, Order, OrderItem, OrderUpdateStatus 
from ..model.cart import Cart, CartItem
from fastapi import Depends, UploadFile, File, Form, HTTPException
from ..utils.admin_verify import get_current_active_admin_user
from ..utils.user_verify import get_current_active_user
from ..model.authentication import Users, Admin
from typing import Annotated, Optional, List
from ..core.db import DB_SESSION
from sqlmodel import select
import json


async def create_order(order_model: OrderModel, user_id: int, session: DB_SESSION):
    order_item_table: List[OrderItem] = []
    try:
        # Check for an existing cart 
        user_cart = session.exec(select(Cart).where(Cart.user_id == user_id)).first()

        if user_cart:
            # Delete cart items
            cart_items = session.exec(select(CartItem).where(CartItem.cart_id == user_cart.id)).all()

            for cart_item in cart_items:
                session.delete(cart_item)

            # Delete the cart
            session.delete(user_cart)

        # Check stock levels and prepare order items
        for order_items in order_model.items:
            product_item = session.exec(select(ProductItem).where(ProductItem.id == order_items.product_item_id)).first()

            if not product_item:
                raise HTTPException(status_code=404, detail="Product item not found")
            
            product = session.exec(select(Product).where(Product.id == order_items.product_id)).first()

            if not product:
                raise HTTPException(status_code=404, detail="Product not found")

            product_size = session.exec(select(ProductSize).where(ProductSize.id == order_items.product_size_id)).first()

            if not product_size:
                raise HTTPException(status_code=404, detail="Product size not found")

            stock = session.exec(select(Stock).where(Stock.product_size_id == product_size.id)).first()
            
            if not stock:
                raise HTTPException(status_code=404, detail="Stock not found")
            
            if stock.stock < order_items.quantity:
                raise HTTPException(status_code=400, detail=f"Product ID {order_items.product_id}, Item ID {order_items.product_item_id}, Size ID {order_items.product_size_id} has low stock. Please order after some time.")
            
            order_item = OrderItem(
                product_id=order_items.product_id,
                product_item_id=order_items.product_item_id,
                product_size_id=order_items.product_size_id,
                quantity=order_items.quantity,
            )
            order_item_table.append(order_item)
            stock.stock -= order_items.quantity  # Reduce the stock

        # Create order
        order = Order(
            order_address=order_model.order_address,
            phone_number=order_model.phone_number,
            order_payment=order_model.order_payment,
            total_price=order_model.total_price,
            user_id=user_id,
            order_items=order_item_table,
        )
        session.add(order)
        session.commit()
        session.refresh(order)

        return {'message': "Order Proceed Successfully!"}

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Order not created: {e}")