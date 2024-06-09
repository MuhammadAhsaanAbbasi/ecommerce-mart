from aiokafka import AIOKafkaProducer # type: ignore

async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers='kafka:19092')
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()