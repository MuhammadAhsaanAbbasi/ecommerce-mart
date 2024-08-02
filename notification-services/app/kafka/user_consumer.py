from app import user_pb2 # Ensure this is the correct path to your generated file

# Other necessary imports
import requests
from typing import Annotated
from aiokafka import AIOKafkaConsumer # type: ignore
from aiokafka.errors import KafkaConnectionError # type: ignore
from fastapi import HTTPException
# from ..schemas.user_emails import email_signup
from app.model.authentication import EmailUser as EmailUserModel
from ..schemas.user_emails import verified_user_schema 
from app.setting import USER_SIGNUP_VERIFY_TOPIC
from ..core.config import send_email_via_ses

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

async def user_consumer():
    consumer_kafka = await get_kafka_consumer([USER_SIGNUP_VERIFY_TOPIC])
    try:
        async for msg in consumer_kafka:
            new_user = user_pb2.EmailUser()  # Correct instantiation
            new_user.ParseFromString(msg.value)
            user_data = EmailUserModel(
                username=new_user.username,
                email=new_user.email,
                imageUrl=new_user.imageUrl,
                is_active=new_user.is_active,
                is_verified=new_user.is_verified,
                role=new_user.role
            )
            print(f"User Data: {user_data}")
            try:
                schema = verified_user_schema(user_data.username)
                send_email = await send_email_via_ses(user_email="", body=schema, subject="User Verified Email")
                print(f"Send Email: {send_email}")
            except HTTPException as e:
                print(e)
    except KafkaConnectionError as e:
        print(f"Error connecting to Kafka: {e}")
    finally:
        await consumer_kafka.stop()