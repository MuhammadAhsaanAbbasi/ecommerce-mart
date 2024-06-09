import json
from typing import Annotated
from aiokafka import AIOKafkaConsumer # type: ignore
from aiokafka.errors import KafkaConnectionError # type: ignore
from fastapi import Depends
from app.service.auth import create_user
from app.model.models import Users
# from app.controllers.kong_controller import create_consumer_in_kong, create_jwt_credential_in_kong
from app.setting import KONG_TOPIC, USER_SIGNUP_TOPIC, USER_SIGNIN_TOPIC, USER_GOOGLE_TOPIC, USER_OTP_TOPIC
from app.kafka.user_producer import get_kafka_producer
from app import user_pb2

###################################################################################################################
async def get_kafka_consumer(topics: str | list[str]):
    consumer_kafka = AIOKafkaConsumer(
        *topics,
        bootstrap_servers="kafka:19092",
        auto_offset_reset="earliest",
        # group_id="user",
    )
    print("Creating Kafka Consumer...")
    await consumer_kafka.start()
    return consumer_kafka
###################################################################################################################


async def user_consumer():
    # consumer_kafka = AIOKafkaConsumer(
    #     "user",
    #     bootstrap_servers="broker:19092",
    #     auto_offset_reset="earliest",
    #     # group_id="user",
    # )
    # print("Creating Kafka Consumer...")
    # await consumer_kafka.start()
    consumer_kafka = await get_kafka_consumer(USER_SIGNUP_TOPIC)
    print("Topic Created SuccessFully")
    try:
        async for msg in consumer_kafka:
            print("Listening...")
            new_user = user_pb2.User()
            new_user.ParseFromString(msg.value)
            # value = bytes(msg.value).decode('utf-8')  # type: ignore
            # user = add_user_in_db(user_form=json.loads(value))
            user_data = Users(username=new_user.username, email=new_user.email, hashed_password=new_user.hashed_password, imageUrl=new_user.imageUrl, is_active=new_user.is_active, is_verified=new_user.is_verified, role=new_user.role)
            user = create_user(user_data)
            # await producer(message=user, topic=KONG_TOPIC)
            print(msg.value)
    except KafkaConnectionError as e:
        print(e)
    finally:
        await consumer_kafka.stop()
        return user