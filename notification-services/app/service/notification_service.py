from ..kafka.user_consumer import user_verified_consumer, user_signup_consumer
from ..kafka.product_consumer import product_consumer
import asyncio

async def task_initiators():
    asyncio.create_task(user_verified_consumer())
    asyncio.create_task(user_signup_consumer())
    asyncio.create_task(product_consumer())