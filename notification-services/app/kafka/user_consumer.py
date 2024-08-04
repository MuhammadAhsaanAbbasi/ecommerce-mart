from app.model.authentication import EmailUser as EmailUserModel, Otp
from aiokafka.errors import KafkaConnectionError # type: ignore
from app.setting import USER_SIGNUP_VERIFY_TOPIC, OTP_TOPIC
from ..schemas.user_emails import verified_user_schema 
from ..utils.actions import send_otp_notification_func
from aiokafka import AIOKafkaConsumer # type: ignore
from ..core.config import send_email_via_ses
from app import user_pb2 # type: ignore
from fastapi import HTTPException


################################################################################################################

async def get_kafka_consumer(topics: list[str]) -> AIOKafkaConsumer:
    consumer_kafka = AIOKafkaConsumer(
        *topics,
        group_id="ecommerce-mart",
        bootstrap_servers="kafka:19092",
        auto_offset_reset="earliest",
    )
    await consumer_kafka.start()
    return consumer_kafka

################################################################################################################

async def user_signup_consumer():
    consumer_kafka = await get_kafka_consumer([OTP_TOPIC])
    try:
        async for msg in consumer_kafka:
            new_user = user_pb2.Otp()  # Correct instantiation
            new_user.ParseFromString(msg.value)
            user_data = Otp(
                email=new_user.email,
                token=new_user.token,
                otp=new_user.otp,
            )
            print(f"User Data: {user_data}")
            try:
                send_email = await send_otp_notification_func(user_email=user_data.email, otp=user_data.otp, token=user_data.token, subject="OTP Notification")
                print(f"Send Email: {send_email}")
            except HTTPException as e:
                print(e)
    except KafkaConnectionError as e:
        print(f"Error connecting to Kafka: {e}")
    finally:
        await consumer_kafka.stop()

################################################################################################################

async def user_verified_consumer():
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
                send_email = await send_email_via_ses(user_email=user_data.email, body=schema, subject="User Verified Email")
                print(f"Send Email: {send_email}")
            except HTTPException as e:
                print(e)
    except KafkaConnectionError as e:
        print(f"Error connecting to Kafka: {e}")
    finally:
        await consumer_kafka.stop()