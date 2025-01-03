from ..model.product import Product, ProductItem, ProductSize, Stock, SizeModel, ProductItemFormModel, ProductFormModel, Size
from ..order_pb2 import OrderBase as OrderBaseProto, OrderItemForm as OrderItemFormProto, OrderModel as OrderModelProto # type: ignore
from ..transaction_pb2 import TransactionModelProto, TransactionProto as Transaction # type: ignore
from ..model.order import OrderModel, Order, OrderItem, OrderUpdateStatus, OrderItemMetadata, OrderMetadata, OrderStatus
from ..model.transaction import TransactionModel, Transaction, TransactionDetail, RefundDetails, Refund
from ..service.payment_service import get_transaction_details
from ..kafka.producer import AIOKafkaProducer, get_kafka_producer 
from ..utils.admin_verify import get_current_active_admin_user
from ..utils.user_verify import get_current_active_user
from fastapi import Depends, HTTPException, Query
from ..model.authentication import Users, Admin
from typing import Annotated, Optional, List
from ..core.db import DB_SESSION
from datetime import datetime
from sqlmodel import select
import json
import uuid

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
        
        transactions_details = []
        for transaction in transactions:
            transaction_details = await get_transaction_details(transaction, session)
            
            transactions_details.append(
                transaction_details
            )
        
        return transactions_details
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_all_refunds_details(session: DB_SESSION,
                        current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
                        from_date: Optional[datetime] = Query(None),
                        to_date: Optional[datetime] = Query(None)):
    if not current_admin:
        raise HTTPException(status_code=403, detail="Unauthorized access")

    query = select(Refund)

    if from_date:
        query = query.where(Refund.refund_date >= from_date)
    if to_date:
        query = query.where(Refund.refund_date <= to_date)

    refunds = session.exec(query).all() 
    
    refunds_details = []
    for refund in refunds:
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
        refunds_details.append(refund_details)
    
    return refunds_details