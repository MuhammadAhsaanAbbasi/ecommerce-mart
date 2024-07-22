# Other necessary imports
from aiokafka.errors import KafkaConnectionError # type: ignore
from aiokafka import AIOKafkaConsumer # type: ignore
from ..model.transaction import TransactionModel
from ..utils.actions import create_transactions
from app import transaction_pb2 # type: ignore
from app.setting import PAYMENT_TOPIC
from fastapi import HTTPException
from ..core.db import engine
from sqlmodel import Session

###################################################################################################################
async def get_kafka_consumer(topics: list[str]) -> AIOKafkaConsumer:
    consumer_kafka = AIOKafkaConsumer(
        *topics,
        group_id="ecommerce-mart",
        bootstrap_servers="kafka:19092",
        auto_offset_reset="earliest",
    )
    await consumer_kafka.start()
    return consumer_kafka

###################################################################################################################

async def payment_consumer():
    consumer_kafka = await get_kafka_consumer([PAYMENT_TOPIC])
    try:
        async for msg in consumer_kafka:
            payment_proto = transaction_pb2.ProductItemFormProtoModel()
            payment_proto.ParseFromString(msg.value)

            user_id = payment_proto.userId

            # Construct ProductItemFormModel from protobuf message
            payment_form = TransactionModel(
                stripeId=payment_proto.stripeId,
                orderId=payment_proto.orderId,
                amount=payment_proto.amount
            )

            with Session(engine) as session:
                transaction = await create_transactions(session, user_id, payment_form)

                print(f"Transaction created: {transaction}")
    except KafkaConnectionError as e:
        print(f"Error connecting to Kafka: {e}")
    finally:
        await consumer_kafka.stop()