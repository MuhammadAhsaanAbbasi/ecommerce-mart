from ..model.product import Product, ProductItem, ProductSize, Stock, SizeModel, ProductItemFormModel, ProductFormModel, Size
from ..order_pb2 import OrderBase as OrderBaseProto, OrderItemForm as OrderItemFormProto, OrderModel as OrderModelProto # type: ignore
from ..model.order import OrderModel, Order, OrderItem, OrderUpdateStatus, OrderItemMetadata, OrderMetadata, OrderStatus
from ..transaction_pb2 import TransactionModelProto, TransactionProto as Transaction # type: ignore
from ..model.transaction import TransactionModel, TransactionDetail
from ..kafka.producer import AIOKafkaProducer, get_kafka_producer 
from ..utils.admin_verify import get_current_active_admin_user
from ..utils.user_verify import get_current_active_user
from fastapi import Depends, HTTPException, Query
from ..setting import ORDER_TOPIC, PAYMENT_TOPIC
from ..model.authentication import Users, Admin
from typing import Annotated, Optional, List
from ..core.db import DB_SESSION
from datetime import datetime
from sqlmodel import select
import json
import uuid

# Create Transaction
async def create_transaction(
        transaction_details: TransactionModel,
        user_id: int,
        aio_producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
):
    try:
        transaction_proto_details = Transaction(
                TransactionModel=TransactionModelProto(
                    stripeId=transaction_details.stripeId,
                    amount=transaction_details.amount,
                    order_id=transaction_details.order_id
                ),
                user_id=user_id
            )
        
        serialized_transaction = transaction_proto_details.SerializeToString()

        # Send order details to Kafka
        await aio_producer.send_and_wait(topic=PAYMENT_TOPIC, value=serialized_transaction)

        
    except HTTPException as e:
        raise e

# Create Transaction & Order
async def create_transaction_order(
        order_details: OrderMetadata,
        transaction_details: TransactionModel,
        aio_producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
):
    try:
        order_proto_details = OrderModelProto(
                user_id=order_details.user_id,
                order_id=order_details.order_id,
                base=OrderBaseProto(
                    order_address=order_details.order_address,
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
        
        serialized_order = order_proto_details.SerializeToString()

        # Send order details to Kafka
        await aio_producer.send_and_wait(topic=ORDER_TOPIC, value=serialized_order)

        await create_transaction(transaction_details, order_details.user_id, aio_producer)

        
    except HTTPException as e:
        raise e

# Get Transaction Details
async def get_transaction_details(transaction: Transaction, session: DB_SESSION):
    user = session.exec(select(Users).where(Users.id == transaction.user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    order = session.exec(select(Order).where(Order.order_id == transaction.order_id)).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    transaction_details = TransactionDetail(
        transaction_id=transaction.transaction_id,
        stripeId=transaction.stripeId,
        amount=transaction.amount,
        order_id=transaction.order_id,
        user_id=transaction.user_id,
        username=user.username,
        email=user.email,
        imageUrl=user.imageUrl,
        order_address=order.order_address,
        phone_number=order.phone_number,
        total_price=order.total_price,
        order_status=order.order_status,
        delivery_date=order.delivery_date,
        order_date=order.order_date
    )

    return transaction_details