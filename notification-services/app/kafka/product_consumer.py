# Other necessary imports
from aiokafka import AIOKafkaConsumer # type: ignore
from aiokafka.errors import KafkaConnectionError # type: ignore
from fastapi import HTTPException
from app.model.models import ProductBaseForm, ProductFormModel, ProductItemFormModel, SizeModel
from app.setting import PRODUCT_TOPIC
from app import product_pb2 # type: ignore
import resend # type: ignore
import requests

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

async def product_consumer():
    consumer_kafka = await get_kafka_consumer([PRODUCT_TOPIC])
    try:
        async for msg in consumer_kafka:
            product_proto = product_pb2.ProductFormModel()
            product_proto.ParseFromString(msg.value)

            # Construct ProductFormModel from protobuf message
            product_form = ProductFormModel(
                product_name=product_proto.product_name,
                product_desc=product_proto.product_desc,
                category_id=product_proto.category_id,
                gender_id=product_proto.gender_id,
                product_item=[
                    ProductItemFormModel(
                        color=item.color,
                        image_url=item.image_url,
                        sizes=[
                            SizeModel(size=size.size, price=size.price, stock=size.stock)
                            for size in item.sizes
                        ]
                    )
                    for item in product_proto.product_item
                ]
            )

            print(f"Product Form Model: {product_form}")

    except KafkaConnectionError as e:
        print(f"Error connecting to Kafka: {e}")
    finally:
        await consumer_kafka.stop()