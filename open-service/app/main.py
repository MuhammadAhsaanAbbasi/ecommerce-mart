from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .web.routes  import router
from .core.db import create_db_and_tables
from .model.transaction import *
from .kafka.payment import payment_consumer
import asyncio

async def task_initiator():
    asyncio.create_task(payment_consumer())


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Hello World..!!!")
    create_db_and_tables()
    await task_initiator()
    yield

app = FastAPI(
    title="Open Service",
    description="This is a Open Service",
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
    root_path="/payment-service",
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

app.router.include_router(router, tags=["Open Services"])

@app.get("/")
def get_root():
    return {"message": "welcome to Open Services! Featured Products, all Products, all categories"}