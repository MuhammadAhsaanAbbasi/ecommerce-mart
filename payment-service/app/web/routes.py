from ..model.transaction import TransactionModel, Transaction, TransactionDetail
from fastapi import APIRouter, Response, HTTPException, Request, Depends, Query
from stripe.error import SignatureVerificationError # type: ignore
from ..kafka.producer import AIOKafkaProducer, get_kafka_producer
from ..setting import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET
from ..service.payment_service import create_transaction_order
from ..utils.admin_verify import get_current_active_admin_user
from typing import Annotated, Optional, List, Sequence
from ..utils.actions import get_transactionBy_date
from ..model.authentication import Users, Admin
from ..model.order import OrderMetadata, Order
from fastapi.responses import JSONResponse
from ..core.db import DB_SESSION
from datetime import datetime
from sqlmodel import select
import json
import stripe

stripe.api_key = STRIPE_SECRET_KEY
router = APIRouter(prefix="/api/v1/payment")

@router.post("/stripe/webhook")
async def payment_webhook(request: Request, 
                        aio_producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event['type'] == 'checkout.session.completed':
        session_data = event['data']['object']
        
        # Extract and parse metadata
        metadata = session_data['metadata']
        items_json = json.loads(metadata['items'])  # Parse the items JSON string
        order_metadata = OrderMetadata(
            user_id=int(metadata['user_id']),
            order_id=metadata['order_id'],
            order_address=metadata['order_address'],
            phone_number=metadata['phone_number'],
            total_price=session_data['amount_total'],
            order_payment=metadata['order_payment'],
            items=items_json  # This should be a list of dictionaries
        )
        
        # Store the transaction
        transaction_model = TransactionModel(
            stripe_id=session_data['id'],
            amount=session_data['amount_total'],
            order_id=metadata['order_id'],
        )

        transaction = await create_transaction_order(order_metadata, transaction_model, aio_producer)

        return JSONResponse(content={"message": "OK", "transaction": transaction})

    return Response(content="", status_code=200)


@router.get("/transaction/all", response_model=List[TransactionDetail])
async def get_all_transactions(
    session: DB_SESSION,
    current_admin: Annotated[Admin, Depends(get_current_active_admin_user)],
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None)
):
    transaction = await get_transactionBy_date(session, current_admin, from_date, to_date)
    return transaction


@router.get("/transaction/specific/{transaction_id}")
async def get_transaction(transaction_id: str, session: DB_SESSION):
    transaction = session.exec(select(Transaction).where(Transaction.transaction_id == transaction_id)).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.get("/transaction/order/{order_id}")
async def get_transaction_by_order(order_id: str, session: DB_SESSION):
    transaction = session.exec(select(Transaction).where(Transaction.order_id == order_id)).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction