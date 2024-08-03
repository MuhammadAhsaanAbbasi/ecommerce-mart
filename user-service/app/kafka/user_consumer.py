from typing import Annotated
from aiokafka import AIOKafkaConsumer # type: ignore
from aiokafka.errors import KafkaConnectionError, KafkaTimeoutError # type: ignore
from fastapi import HTTPException
from app.service.auth import create_user
from app.model.models import Users
from app.setting import USER_SIGNUP_TOPIC, OTP_TOPIC
from app.kafka.user_producer import aio_producer
from app import user_pb2
from ..user_pb2 import Otp as OtpProto  # type: ignore
from sqlmodel import Session
from ..core.db import engine

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
            token=new_user.token
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
                    print(f"Created user: {user.otp}") 

                    try:
                        otp_protobuf = OtpProto(
                                                email=user_data.email,
                                                token=token,
                                                otp=user.otp,
                                                    )
                        print(f"Todo Protobuf: {otp_protobuf}")

                        # Serialize the message to a byte string
                        serialized_otp = otp_protobuf.SerializeToString()
                        print(f"Serialized data: {serialized_otp}")

                        # Produce message
                        await aio_producer.send_and_wait(topic=OTP_TOPIC, value=serialized_otp)
                    except KafkaTimeoutError as e:
                        print(f"Error In Print message...! {e}")
                    finally:
                        await aio_producer.stop()

                except HTTPException as e:
                    print(f"Error creating user: {e.detail}")
    except KafkaConnectionError as e:
        print(f"Error connecting to Kafka: {e}")
    finally:
        await consumer_kafka.stop()