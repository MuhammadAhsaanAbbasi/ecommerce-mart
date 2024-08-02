# Other necessary imports
from aiokafka import AIOKafkaConsumer # type: ignore
from aiokafka.errors import KafkaConnectionError # type: ignore
from fastapi import HTTPException
from app.model.models import ProductBaseForm, ProductFormModel, ProductItemFormModel, SizeModel
from ..service.product_service import send_product_email
from app.setting import PRODUCT_TOPIC
from app import product_pb2 # type: ignore
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
                featured=product_proto.featured,
                category_id=product_proto.category_id,
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
            print(f"Product Form Image: {product_form.product_item[0].image_url}")
            print(f"Product Form Prize: {product_form.product_item[0].sizes[0].price}")

            with Session(engine) as session:
                try:
                    email_sent = await send_product_email(product_form, session=session)
                    # print(f"Created user: {email_sent}") 

                except HTTPException as e:
                    print(f"Error creating user: {e.detail}")

            print(f"email_sent: {email_sent}")

    except KafkaConnectionError as e:
        print(f"Error connecting to Kafka: {e}")
    finally:
        await consumer_kafka.stop()