# Other necessary imports
from aiokafka import AIOKafkaConsumer # type: ignore
from aiokafka.errors import KafkaConnectionError # type: ignore
from fastapi import HTTPException
# from app.utils.auth import email_signup
from app.model.models import ProductBaseForm, ProductFormModel, ProductItemFormModel, SizeModel
from app.setting import INVENTORY_TOPIC
from app import inventory_pb2 # type: ignore
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

async def product_item_consumer():
    consumer_kafka = await get_kafka_consumer([INVENTORY_TOPIC])
    try:
        async for msg in consumer_kafka:
            product_item_proto = inventory_pb2.ProductItemFormProtoModel()
            product_item_proto.ParseFromString(msg.value)

            # Construct ProductItemFormModel from protobuf message
            product_item_form = ProductItemFormModel(
                product_id=product_item_proto.product_id,
                color=product_item_proto.color,
                image_url=product_item_proto.image_url,
                sizes=[
                    SizeModel(size=size.size, price=size.price, stock=size.stock)
                    for size in product_item_proto.sizes
                ]
            )

            print(f"Product Item Form Model: {product_item_form}")

    except KafkaConnectionError as e:
        print(f"Error connecting to Kafka: {e}")
    finally:
        await consumer_kafka.stop()