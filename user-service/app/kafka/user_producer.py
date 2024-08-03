from aiokafka import AIOKafkaProducer # type: ignore
from typing import AsyncGenerator, Annotated
from fastapi import Depends

async def get_kafka_producer() -> AsyncGenerator[AIOKafkaProducer, None]:
    producer = AIOKafkaProducer(bootstrap_servers='kafka:19092')
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

aio_producer = Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]