# Other necessary imports
from aiokafka import AIOKafkaConsumer # type: ignore
from aiokafka.errors import KafkaConnectionError # type: ignore
from fastapi import HTTPException
from ..model.order import OrderModel, OrderItemForm, OrderBase, OrderPayment
from ..utils.actions import create_order
from app.setting import ORDER_TOPIC
from app import order_pb2 # type: ignore
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

async def order_consumer():
    consumer_kafka = await get_kafka_consumer([ORDER_TOPIC])
    try:
        async for msg in consumer_kafka:
            order_proto = order_pb2.OrderModelProto()
            order_proto.ParseFromString(msg.value)

            # Construct OrderModel from protobuf message
            order_id = order_proto.order_id
            order_base = order_proto.base
            order_model = OrderModel(
                order_address=order_base.order_address,
                phone_number=order_base.phone_number,
                total_price=order_base.total_price,
                order_payment=OrderPayment(order_base.order_payment.name),
                items=[
                    OrderItemForm(
                        product_id=item.product_id,
                        product_item_id=item.product_item_id,
                        product_size_id=item.product_size_id,
                        quantity=item.quantity
                    ) for item in order_proto.items
                ]
            )

            print(f"Order Model: {order_model}")

            with Session(engine) as session:
                try:
                    user = create_order(order_model, session)
                    # print(f"Created user: {user['data']['email']}")
                except HTTPException as e:
                    print(f"Error creating user: {e.detail}")

    except KafkaConnectionError as e:
        print(f"Error connecting to Kafka: {e}")
    finally:
        await consumer_kafka.stop()