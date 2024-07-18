from ..model.product import Product, ProductItem, ProductSize, Stock, SizeModel, ProductItemFormModel, ProductFormModel, Size
from ..order_pb2 import OrderBase as OrderBaseProto, OrderItemForm as OrderItemFormProto, OrderModel as OrderModelProto # type: ignore
from ..transaction_pb2 import TransactionModelProto, TransactionProto as Transaction # type: ignore
from ..model.order import OrderModel, Order, OrderItem, OrderUpdateStatus, OrderItemMetadata, OrderMetadata, OrderStatus
from ..model.transaction import TransactionModel, Transaction
from ..kafka.producer import AIOKafkaProducer, get_kafka_producer 
from ..utils.admin_verify import get_current_active_admin_user
from ..utils.user_verify import get_current_active_user
from ..model.authentication import Users, Admin
from typing import Annotated, Optional, List
from fastapi import Depends, HTTPException
from ..setting import ORDER_TOPIC, PAYMENT_TOPIC
from ..core.db import DB_SESSION
from sqlmodel import select
import json
import uuid

async def create_transactions(transaction_details: TransactionModel, 
                                user_id: int, 
                                session: DB_SESSION):
    transaction = Transaction(
        user_id=user_id,
        **transaction_details.model_dump()
    )
    session.add(transaction)
    session.commit()
    session.refresh(transaction)

    return {"message" : "Successfully Charged transaction", "data" : transaction}