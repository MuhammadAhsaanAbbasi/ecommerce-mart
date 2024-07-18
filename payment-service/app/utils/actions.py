from ..model.product import Product, ProductItem, ProductSize, Stock, SizeModel, ProductItemFormModel, ProductFormModel, Size
from ..order_pb2 import OrderBase as OrderBaseProto, OrderItemForm as OrderItemFormProto, OrderModel as OrderModelProto # type: ignore
from ..transaction_pb2 import TransactionModelProto, TransactionProto as Transaction # type: ignore
from ..model.order import OrderModel, Order, OrderItem, OrderUpdateStatus, OrderItemMetadata, OrderMetadata, OrderStatus
from ..model.transaction import TransactionModel, Transaction, TransactionDetail
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

async def get_transactionBy_date(
    session: DB_SESSION,
    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None)
):
    if not current_admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    
    if not Transaction.created_at:
        raise HTTPException(status_code=400, detail="Order date not found")
    
    try:
        query = select(Transaction)
        
        if from_date:
            query = query.where(Transaction.created_at >= from_date)
        if to_date:
            query = query.where(Transaction.created_at <= to_date)

        transactions = session.exec(query).all()
        
        transaction_details = []
        for transaction in transactions:
            user = session.exec(select(Users).where(Users.id == transaction.user_id)).first()
            if not user:
                continue

            order = session.exec(select(Order).where(Order.order_id == transaction.order_id)).first()
            if not order:
                continue
            
            transaction_details.append(
                TransactionDetail(
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
            ))
        
        return transaction_details
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))