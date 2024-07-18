from fastapi import APIRouter, Response, HTTPException, Request, Depends
from ..kafka.producer import AIOKafkaProducer, get_kafka_producer
from ..service.payment_service import create_transaction_order
from ..setting import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET
from stripe.error import SignatureVerificationError # type: ignore
from ..model.transaction import TransactionModel, Transaction
from typing import Annotated, Optional, List, Sequence
from fastapi.responses import JSONResponse
from ..model.order import OrderMetadata
from ..core.db import DB_SESSION
from sqlmodel import Session, select
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


@router.get("/transaction/all", response_model=Sequence[Transaction])
async def get_all_transactions(session: Session):
    transactions = session.exec(select(Transaction)).all()
    return transactions
