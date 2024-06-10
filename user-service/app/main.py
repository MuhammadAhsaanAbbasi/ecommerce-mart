from fastapi import FastAPI, Depends
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .web.route  import router
from .web.admin_route import admin_router
from .core.db import create_db_and_tables, get_session, DB_SESSION
from .kafka.user_consumer import user_consumer
from .model.models import Users
from sqlmodel import Session
from typing import Annotated
import asyncio

async def task_initiator():
    asyncio.create_task(user_consumer())

@asynccontextmanager
async def life_span(app: FastAPI):
    print("Hello World..!!!")
    create_db_and_tables()
    await task_initiator()
    yield

app = FastAPI(
    title="User Service",
    description="User Micro-Service that authenticate and authorize user for authentication & authorization & return access token to access other Micro-Services",
    version="1.0.0",
    terms_of_service="https://caxgpt.vercel.app/terms/",
    lifespan=life_span,
    contact={
        "name": "Muhammad Ahsaan Abbasi",
        "phone": "+92 349-204-7381",
        "email": "mahsaanabbasi@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    },
    root_path="/user-service",
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

app.router.include_router(router=router, tags=["User Authorize & Authentication"])
app.include_router(router=admin_router, tags=["Admin Authorize & Authentication"])

@app.get("/")
def get_root():
    return {"message": "welcome to login & Sign-up System & User Service"}