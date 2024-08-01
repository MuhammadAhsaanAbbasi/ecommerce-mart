from app import user_pb2 # Ensure this is the correct path to your generated file

# Other necessary imports
import requests
from typing import Annotated
from aiokafka import AIOKafkaConsumer # type: ignore
from aiokafka.errors import KafkaConnectionError # type: ignore
from fastapi import HTTPException
# from ..schemas.user_emails import email_signup
from app.model.models import EmailUser as EmailUserModel
from app.setting import USER_SIGNUP_EMAIL_TOPIC
from sqlmodel import Session
from ..core.db import DB_SESSION, engine
import resend # type: ignore 

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
    consumer_kafka = await get_kafka_consumer([USER_SIGNUP_EMAIL_TOPIC])
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
            # try:
            #     # Send OTP to user
            #     params = {
            #         "from": "onboarding@resend.dev",
            #         "to": [user_data.email],  # Use user email dynamically
            #         "subject": "Congratulations! Email",
            #         "html": f"<p>Congratulations on successfully verifying your email address. We are thrilled to have you with us!</p>",
            #     }
            #     response = resend.Emails.send(params)
            #     print(response)
            # except HTTPException as e:
            #     print(e)
    except KafkaConnectionError as e:
        print(f"Error connecting to Kafka: {e}")
    finally:
        await consumer_kafka.stop()