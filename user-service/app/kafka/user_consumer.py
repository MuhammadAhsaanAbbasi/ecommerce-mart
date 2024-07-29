import requests
from typing import Annotated
from aiokafka import AIOKafkaConsumer # type: ignore
from aiokafka.errors import KafkaConnectionError # type: ignore
from fastapi import HTTPException
from app.service.auth import create_user
from app.model.models import Users
from app.setting import USER_SIGNUP_TOPIC
from app.kafka.user_producer import get_kafka_producer
from app import user_pb2
from sqlmodel import Session
from ..core.db import DB_SESSION, engine

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
    consumer_kafka = await get_kafka_consumer([USER_SIGNUP_TOPIC])
    try:
        async for msg in consumer_kafka:
            new_user = user_pb2.User()
            new_user.ParseFromString(msg.value)
            user_data = Users(username=new_user.username, 
                                    email=new_user.email, 
                                    hashed_password=new_user.hashed_password, 
                                    imageUrl=new_user.imageUrl,
                                    phone_number=new_user.phone_number,
                                    date_of_birth=new_user.date_of_birth,
                                    gender=new_user.gender,
                                    )
            with Session(engine) as session:
                try:
                    user = await create_user(user_data, session)
                    print(f"Created user: {user}") 

                except HTTPException as e:
                    print(f"Error creating user: {e.detail}")
    except KafkaConnectionError as e:
        print(f"Error connecting to Kafka: {e}")
    finally:
        await consumer_kafka.stop()