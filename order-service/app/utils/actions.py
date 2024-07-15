from ..model.product import Product, ProductItem, ProductSize, Stock, SizeModel, ProductItemFormModel, ProductFormModel, Size
from ..model.order import OrderModel, Order, OrderItem, OrderUpdateStatus, OrderItemDetail, OrderDetail
from ..setting import STRIPE_SECRET_KEY, NEXT_PUBLIC_APP_URL
from fastapi.responses import RedirectResponse
from fastapi import Depends, HTTPException
from ..model.cart import Cart, CartItem
from typing import List, Sequence
from ..core.db import DB_SESSION
from sqlmodel import select
import json 
import stripe

stripe.api_key = STRIPE_SECRET_KEY

async def create_order(order_model: OrderModel, user_id: int, session: DB_SESSION):
    order_item_table: List[OrderItem] = []
    try:
        # Check for an existing cart 
        user_cart = session.exec(select(Cart).where(Cart.user_id == user_id)).first()

        # Check stock levels and prepare order items
        for order_items in order_model.items:
            product_item = session.exec(select(ProductItem).where(ProductItem.product_item_id == order_items.product_item_id)).first()

            if not product_item:
                raise HTTPException(status_code=404, detail="Product item not found")
            
            product = session.exec(select(Product).where(Product.product_id == order_items.product_id)).first()

            if not product:
                raise HTTPException(status_code=404, detail="Product not found")

            product_size = session.exec(select(ProductSize).where(ProductSize.product_size_id == order_items.product_size_id)).first()

            if not product_size:
                raise HTTPException(status_code=404, detail="Product size not found")

            

            stock = session.exec(select(Stock).where(Stock.product_size_id == product_size.id)).first()
            
            if not stock:
                raise HTTPException(status_code=404, detail="Stock not found")
            
            if stock.stock < order_items.quantity:
                size = session.exec(select(Size).where(Size.id == product_size.size)).first()
                raise HTTPException(status_code=400, detail=f"You Select Product {product.product_name}, have color {product_item.color} in {size.size if size else ""} Size has low stock. Please order after some Days.")
            
            if user_cart:
            # Delete cart items
                cart_items = session.exec(select(CartItem).where(CartItem.cart_id == user_cart.id)).all()

                order_items_set = {
                    (item.product_item_id, item.product_size_id, item.quantity)
                    for item in order_model.items
                }

                # Delete only matching cart items
                for cart_item in cart_items:
                    if (cart_item.product_item_id, cart_item.product_size_id, cart_item.quantity) in order_items_set:
                        session.delete(cart_item)

                # If all items in the cart are deleted, delete the cart itself
                remaining_cart_items_query = select(CartItem).where(CartItem.cart_id == user_cart.id)
                remaining_cart_items = session.exec(remaining_cart_items_query).all()

                if not remaining_cart_items:
                    session.delete(user_cart)

            order_item = OrderItem(
                product_id=product.id,
                product_item_id=product_item.id,
                product_size_id=product_size.id,
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

async def all_order_details(user_orders: Sequence[Order], session: DB_SESSION):
    all_order_detail = []

    try:
        for order in user_orders:
            order_items = session.exec(select(OrderItem).where(OrderItem.order_id == order.id)).all()
            order_items_detail = []

            for order_item in order_items:
                product = session.exec(select(Product).where(Product.id == order_item.product_id)).first()
                product_item = session.exec(select(ProductItem).where(ProductItem.id == order_item.product_item_id)).first()
                product_size = session.exec(select(ProductSize).where(ProductSize.id == order_item.product_size_id)).first()
                stock = session.exec(select(Stock).where(Stock.product_size_id == order_item.product_size_id)).first()

                if product and product_item and product_size and stock:
                    size = session.exec(select(Size).where(Size.id == product_size.size)).first()
                    if not size:
                        raise HTTPException(status_code=404, detail="Size not found")

                    order_item_detail = OrderItemDetail(
                        product=product.product_name,
                        product_item={
                            'color': product_item.color,
                            'image_url': product_item.image_url
                        },
                        size=size.size,
                        price=product_size.price,
                        quantity=order_item.quantity,
                        stock=stock.stock,
                    )
                    order_items_detail.append(order_item_detail)

            order_detail = OrderDetail(
                order_id=order.id,
                order_address=order.order_address,
                phone_number=order.phone_number,
                order_payment=order.order_payment,
                total_price=order.total_price,
                order_status=order.order_status,
                tracking_id=order.tracking_id,
                delivery_date=order.delivery_date,
                order_date=order.order_date,
                order_items=order_items_detail
            )
            all_order_detail.append(order_detail)
            
        return all_order_detail
    except HTTPException as e:
        raise e

async def fetch_product_details(product_id: str, 
                                product_item_id: int,
                                product_size_id: int,
                                session: DB_SESSION):
    
    product = session.exec(select(Product).where(Product.product_id == product_id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product_item = session.exec(select(ProductItem).where(ProductItem.id == product_item_id)).first()
    if not product_item:
        raise HTTPException(status_code=404, detail="Product item not found")
    
    product_size = session.exec(select(ProductSize).where(ProductSize.id == product_size_id)).first()
    if not product_size:
        raise HTTPException(status_code=404, detail="Product size not found")
    
    return product_size.price, product_item.image_url, product.product_name

def create_metadata(order_details: OrderModel, user_id: int) -> dict:
    return {
        'user_id': user_id,
        'order_address': order_details.order_address,
        'phone_number': order_details.phone_number,
        'total_price': order_details.total_price,
        'order_payment': order_details.order_payment.value,
        'items': [
            {
                'product_id': item.product_id,
                'product_item_id': item.product_item_id,
                'product_size_id': item.product_size_id,
                'quantity': item.quantity
            }
            for item in order_details.items
        ]
    }

async def order_checkout(order_details: OrderModel, user_id: int, session: DB_SESSION):
    try:
        line_items = []
        for item in order_details.items:
            price, image_url, product = await fetch_product_details(item.product_id, 
                                                        item.product_item_id,
                                                        item.product_size_id, 
                                                        session)
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product,  # Assuming product_id can be used as a name
                        'images': [image_url],
                    },
                    'unit_amount': int(price * 100),  # Convert to cents
                },
                'quantity': item.quantity,
            })
        
        metadata = create_metadata(order_details, user_id)
        
        stripe_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            metadata=metadata,
            mode='payment',
            success_url=f"{NEXT_PUBLIC_APP_URL}/profile",
            cancel_url=f"{NEXT_PUBLIC_APP_URL}/",
        )

        if not stripe_session.url:
            raise HTTPException(status_code=500, detail="Stripe session not created")
        
        response = RedirectResponse(url=stripe_session.url)

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))