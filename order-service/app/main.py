from aiokafka.admin import AIOKafkaAdminClient, NewTopic # type: ignore
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .web.order_routes  import order_router
from .core.db import create_db_and_tables
from .kafka.order import order_consumer
from .web.cart_routes  import router
from .setting import ORDER_TOPIC
from fastapi import FastAPI
from .model.order import *
from .model.cart import *
import asyncio

async def task_initiator():
    asyncio.create_task(order_consumer())

@asynccontextmanager
async def life_span(app: FastAPI):
    print("Hello World..!!!")
    create_db_and_tables()
    await task_initiator()
    yield

app = FastAPI(
    title="Order Service",
    description="This is a Order Service",
    version="1.0.0",
    terms_of_service="https://caxgpt.vercel.app/terms/",
    lifespan=life_span,
    contact={
        "name": "Muhammad Ahsaan Abbasi",
        "email": "mahsaanabbasi@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    },
    root_path="/order-service",
    root_path_in_servers=True,
    docs_url="/docs"
)

# SessionMiddleware must be installed to access request.session
app.add_middleware(
    SessionMiddleware, secret_key="!secret")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PUT"],
    allow_headers=["*"],
)

app.router.include_router(router, tags=["Cart Services"])
app.router.include_router(order_router, tags=["Order Services"])

@app.get("/")
def get_root():
    return {"message": "welcome to Order Services, Create Order, Update Order, Delete Order, User All Orders, User Specific Order Details!!"}