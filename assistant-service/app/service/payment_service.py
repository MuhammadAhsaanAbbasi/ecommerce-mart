from ..model.transaction import TransactionModel, TransactionDetail, Refund, RefundDetails, Transaction
from ..kafka.producer import AIOKafkaProducer, get_kafka_producer 
from ..utils.admin_verify import get_current_active_admin_user
from ..utils.user_verify import get_current_active_user
from fastapi import Depends, HTTPException, Query
from ..model.authentication import Users, Admin
from typing import Annotated, Optional, List
from ..model.order import OrderModel, Order
from ..core.db import DB_SESSION
from datetime import datetime
from sqlmodel import select
import json
import uuid

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

async def get_refunds(refund_id: str, session: DB_SESSION,
                    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)]):
    if not current_admin:
        raise HTTPException(status_code=403, detail="Unauthorized access")
    
    refund = session.exec(
        select(Refund)
        .where(Refund.refund_id == refund_id)
    ).first()

    if not refund:
        raise HTTPException(status_code=404, detail="Refund not found")
    
    order = session.exec(select(Order).where(Order.id == refund.order_id)).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    user = session.exec(select(Users).where(Users.id == refund.user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    
    refund_details = RefundDetails(
        refund_id=refund.refund_id,
        amount=refund.amount,
        stripeId=refund.stripeId,
        status=refund.status,
        reason=refund.reason,
        refund_date=refund.refund_date,
        username=user.username,
        email=user.email,
        imageUrl=user.imageUrl,
        order_address=order.order_address,
        phone_number=order.phone_number,
        order_status=order.order_status,
        delivery_date=order.delivery_date,
        order_date=order.order_date,
        user_id=user.id,
        order_id=order.order_id,
        transaction_id=refund.transaction_id
    )

    return refund_details