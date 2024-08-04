from aiokafka import AIOKafkaProducer # type: ignore
# from aiokafka.partitioner import DefaultPartitioner
from typing import AsyncGenerator

async def get_kafka_producer() -> AsyncGenerator[AIOKafkaProducer, None]:
    producer = AIOKafkaProducer(bootstrap_servers='kafka:19092')
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()