import json
from typing import Annotated
from aiokafka import AIOKafkaConsumer # type: ignore
from aiokafka.errors import KafkaConnectionError # type: ignore
from fastapi import HTTPException
from app.service.auth import create_user
from app.model.models import Users
from app.service.kong_consumer import create_consumer_in_kong, create_jwt_credentials_in_kong
from app.setting import KONG_TOPIC, USER_SIGNUP_TOPIC, USER_SIGNIN_TOPIC, USER_GOOGLE_TOPIC, USER_OTP_TOPIC
from app.kafka.user_producer import get_kafka_producer
from app import user_pb2
from sqlmodel import Session
from ..core.db import DB_SESSION, engine

###################################################################################################################
async def get_kafka_consumer(topics: list[str]) -> AIOKafkaConsumer:
    consumer_kafka = AIOKafkaConsumer(
        *topics,
        bootstrap_servers="kafka:19092",
        auto_offset_reset="earliest",
    )
    await consumer_kafka.start()
    return consumer_kafka

###################################################################################################################

async def user_consumer():
    consumer_kafka = await get_kafka_consumer([USER_SIGNUP_TOPIC])
    try:
        async for msg in consumer_kafka:
            new_user = user_pb2.User()
            new_user.ParseFromString(msg.value)
            user_data = Users(
                username=new_user.username, email=new_user.email, hashed_password=new_user.hashed_password,
                imageUrl=new_user.imageUrl, is_active=new_user.is_active, is_verified=new_user.is_verified, role=new_user.role
            )
            with Session(engine) as session:
                try:
                    user = create_user(user_data, session)
                    print(user)

                    create_consumer_in_kong(user.data.email)
                    create_jwt_credentials_in_kong(user.data.email, user.data.kid)
                except HTTPException as e:
                    print(f"Error creating user: {e}")
            print(msg.value)
    except KafkaConnectionError as e:
        print(e)
    finally:
        await consumer_kafka.stop()