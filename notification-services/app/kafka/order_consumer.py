from app.model.authentication import EmailUser as EmailUserModel, Otp
from ..model.order import OrderModel, OrderItemBase, OrderPayment
from aiokafka.errors import KafkaConnectionError # type: ignore 
from ..service.order_service import send_order_confirmation_email
from aiokafka import AIOKafkaConsumer # type: ignore
from app import order_pb2 # type: ignore
from app.setting import ORDER_TOPIC
from fastapi import HTTPException
from sqlmodel import Session
from ..core.db import engine


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

async def order_consumer():
    consumer_kafka = await get_kafka_consumer([ORDER_TOPIC])
    try:
        async for msg in consumer_kafka:
            order_proto = order_pb2.OrderModel()
            order_proto.ParseFromString(msg.value)

            # Construct OrderModel from protobuf message
            user_id = order_proto.user_id
            order_id = order_proto.order_id
            order_base = order_proto.base
            order_model = OrderModel(
                email=order_base.email,
                country=order_base.country,
                city=order_base.city,
                postal_code=order_base.postal_code,
                address=order_base.address, 
                phone_number=order_base.phone_number, 
                total_price=order_base.total_price,
                order_payment=OrderPayment(order_base.order_payment),
                items=[
                    OrderItemBase(
                        product_id=item.product_id,
                        product_item_id=item.product_item_id,
                        product_size_id=item.product_size_id,
                        quantity=item.quantity
                    ) for item in order_proto.items
                ]
            )

            print(f"Order Model: {order_model}")
            print(f"User Id: {user_id}")
            print(f"Order Id: {order_id}")

            with Session(engine) as session:
                try:
                    order = await send_order_confirmation_email(order_model, user_id, order_id, session)
                    print(f"Created Order: {order}")
                except HTTPException as e:
                    print(f"Error creating user: {e.detail}")

    except KafkaConnectionError as e:
        print(f"Error connecting to Kafka: {e}")
    finally:
        await consumer_kafka.stop()

################################################################################################################