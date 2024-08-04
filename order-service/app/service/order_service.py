from ..model.product import Product, ProductItem, ProductSize, Stock, SizeModel, ProductItemFormModel, ProductFormModel, Size
from ..order_pb2 import OrderBase as OrderBaseProto, OrderItemForm as OrderItemFormProto, OrderModel as OrderModelProto # type: ignore
from ..model.order import OrderModel, Order, OrderItem, OrderItemDetail, OrderDetail, OrderStatus
from ..utils.actions import create_order, all_order_details, order_checkout
from ..kafka.producer import AIOKafkaProducer, get_kafka_producer 
from ..utils.admin_verify import get_current_active_admin_user
from ..utils.user_verify import get_current_active_user
from datetime import datetime, timedelta, timezone
from ..model.authentication import Users, Admin
from typing import Annotated, Optional, List
from fastapi import Depends, HTTPException
from ..setting import ORDER_TOPIC
from ..core.db import DB_SESSION
from sqlmodel import select
import json
import uuid

# Create Orders
async def create_orders(
                    order_details: OrderModel,
                    session: DB_SESSION, 
                    current_user: Annotated[Users, Depends(get_current_active_user)],
                    aio_producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
                    ):

    if current_user.id is None:
        raise HTTPException(status_code=400, detail="User ID is invalid")
    
    try:
        order_id = uuid.uuid4().hex
        print(order_id)
        if order_details.order_payment == "Cash On Delivery":
            # Convert order details to protobuf message
            order_proto = OrderModelProto(
                user_id=current_user.id,
                order_id=order_id,
                base=OrderBaseProto(
                    email=order_details.email,
                    country=order_details.country,
                    city=order_details.city,
                    postal_code=order_details.postal_code,
                    address=order_details.address, 
                    phone_number=order_details.phone_number, 
                    total_price=order_details.total_price,
                    order_payment=order_details.order_payment
                ),
                items=[
                    OrderItemFormProto(
                        product_id=item.product_id,
                        product_item_id=item.product_item_id,
                        product_size_id=item.product_size_id,
                        quantity=item.quantity
                    ) for item in order_details.items
                ]
            ) 

            serialized_order = order_proto.SerializeToString()

            await aio_producer.send_and_wait(topic=ORDER_TOPIC, value=serialized_order)

            return {'message': "Order Proceed Successfully!"}
        else:
            checkout = await order_checkout(order_details, order_id, current_user.id, session)
            return checkout
    except HTTPException as e:
        raise e


async def get_orders_by_user(
        current_user: Annotated[Users, Depends(get_current_active_user)],
        session: DB_SESSION,
        limit: int,
        offset: int,
    ):
    user_orders = session.exec(select(Order).where(Order.user_id == current_user.id).offset(offset).limit(limit)).all()
    if not user_orders:
        raise HTTPException(status_code=404, detail="Order not found")
    order_details = await all_order_details(user_orders, session)
    return order_details


# Get All Orders
async def get_all_orders(
                    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    limit: int,
                    offset: int,
                    ):
    if not current_admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    all_orders = session.exec(select(Order).offset(offset).limit(limit)).all()

    order_details = await all_order_details(all_orders, session)

    return order_details


# Get Order By Id
async def get_orders_by_id(
        session: DB_SESSION,
        order_id: str,
    ):
    order = session.exec(select(Order).where(Order.id == order_id)).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    try:
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

        user = session.exec(select(Users).where(Users.id == order.user_id)).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        order_detail = OrderDetail(
            order_id=order.id,
            address=order.address,
            email=order.email,
            country=order.country,
            city=order.city,
            postal_code=order.postal_code,
            phone_number=order.phone_number,
            order_payment=order.order_payment,
            total_price=order.total_price,
            order_status=order.order_status,
            tracking_id=order.tracking_id,
            delivery_date=order.delivery_date,
            order_date=order.order_date,
            order_items=order_items_detail,
            user_name=user.username,
            user_email=user.email,
            user_image_url=user.imageUrl
        )

        return order_detail
    except HTTPException as e:
        raise e


# Update Order Status
async def update_orders_status(
                    # current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    order_id: str,
                    order_status: OrderStatus
                    ):
    # if not current_admin:
    #     raise HTTPException(status_code=404, detail="Admin not found")

    try:
        # Retrieve the order by order_id
        order = session.exec(select(Order).where(Order.id == order_id)).first()
        
        # Check if the order exists
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Update the status of the order
        if order_status not in OrderStatus.__members__:
            raise HTTPException(status_code=400, detail="Invalid order status")

        order.order_status = OrderStatus[order_status]

        # Commit the changes to the database
        session.add(order)
        session.commit()
        session.refresh(order)
        
        return {'message': "Order status updated successfully!"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update order status: {e}")


# Delete Order
async def delete_orders(
                    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                    session: DB_SESSION,
                    order_id: str,
                    ):
    if not current_admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    try:
        # Retrieve the order by order_id
        order = session.exec(select(Order).where(Order.id == order_id)).first()
        
        # Check if the order exists
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        # Retrieve and delete associated OrderItem entries
        order_items = session.exec(select(OrderItem).where(OrderItem.order_id == order.id)).all()
        
        for order_item in order_items:
            session.delete(order_item)
        
        # Delete the order
        session.delete(order)

        # Commit the changes to the database
        session.commit()
        
        return {'message': "Order and its items deleted successfully!"}
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete order: {e}")


# Fetch Orders
async def fetch_orders(
        # current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
        session: DB_SESSION,
        limit: int,
        offset: int,
        status: Optional[str],
        from_date: Optional[datetime],
        to_date: Optional[datetime]
    ):
    # if not current_admin:
    #     raise HTTPException(status_code=404, detail="Admin not found")
    
    if status and status not in OrderStatus.__members__:
        raise HTTPException(status_code=400, detail="Invalid order status")
    
    if not Order.order_date:
        raise HTTPException(status_code=400, detail="Order date not found")

    try:
        query = select(Order).offset(offset).limit(limit)
        
        if status:
            query = query.where(Order.order_status == status)
        if from_date:
            query = query.where(Order.order_date >= from_date) 
        if to_date:
            query = query.where(Order.order_date <= to_date)
        
        orders = session.exec(query).all()
        
        if not orders:
            raise HTTPException(status_code=404, detail="No orders found with the given criteria")

        order_details = await all_order_details(orders, session)

        return order_details

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to retrieve orders: {e}")


# Customer Cancel Order
async def cancel_orders_by_customer(
                    current_user: Annotated[Users, Depends(get_current_active_user)],
                    session: DB_SESSION,
                    order_id: str,
                    ):
    try:
        # Retrieve the order by order_id
        order = session.exec(select(Order).where(Order.id == order_id)).first()
        
        # Check if the order exists and belongs to the current user
        if not order or order.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Order not found or does not belong to the current user")
        
        # Check if the order_date is within the allowable cancellation period (3 days ago)
        now = datetime.now(timezone.utc)
        if not order.order_date or (now - order.order_date) > timedelta(days=3):
            raise HTTPException(status_code=400, detail="Order cannot be cancelled as it is older than 3 days")
        
        # Cancel the order by setting its status to 'Cancelled'
        order.order_status = OrderStatus.cancelled
        
        # Commit the changes to the database
        session.add(order)
        session.commit()
        session.refresh(order)
        
        return {'message': "Order cancelled successfully!"}
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to cancel order: {e}")

# Function to get user orders by status
async def get_user_orders_by_status(
                    current_user: Annotated[Users, Depends(get_current_active_user)],
                    session: DB_SESSION,
                    status: str,
                    offset: int,
                    limit: int,
                    ):
    # try:
    #     order_status = OrderStatus[status]

    # except KeyError:
    #     raise HTTPException(status_code=400, detail="Invalid order status")

    # if status not in OrderStatus:
    #     raise HTTPException(status_code=400, detail="Invalid order status")
    
    if not Order.order_status:
        raise HTTPException(status_code=400, detail="Order status not found")
    
    query = select(Order).where(Order.user_id == current_user.id).where(Order.order_status == status).offset(offset).limit(limit)

    
    orders = session.exec(query).all()
    
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found with the given status")
    
    order_details = await all_order_details(orders, session)
    
    return order_details