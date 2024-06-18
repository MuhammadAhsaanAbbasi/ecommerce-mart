from fastapi import APIRouter, Depends,  Form, Request, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse, Response
from ..lib.utils import create_categories, get_categories
from ..model.category_model import Category, Size, Gender
# from ..kafka.user_producer import get_kafka_producer
# from aiokafka import AIOKafkaProducer # type: ignore
# from aiokafka.errors import KafkaTimeoutError # type: ignore
from typing import Annotated, Any, Optional
from sqlmodel import Session, select
from ..core.db import get_session
from datetime import timedelta
# from app import user_pb2
import os
import json


# Router
csg_router = APIRouter(prefix="/api/v1")

csg_router.post("/create_category")
async def create_category(category_input: Category, session: Annotated[Session, Depends(get_session)]):
    category = await create_categories(category_input,session)
    return {"message" : "Create Product Category Successfully!", "data": category}

csg_router.get("/get_category")
async def get_category(session: Annotated[Session, Depends(get_session)]):
    category = await get_categories(session)
    return category

csg_router.post("/create_size")
async def create_size(size_input: Size, session: Annotated[Session, Depends(get_session)]):
    # size = await create_sizes(size_input,session)
    return {"message" : "Create Product"}

csg_router.get("/get_sizes")
async def get_sizes(size_input: Size, session: Annotated[Session, Depends(get_session)]):
    # size = await get_size(size_input, session)
    return {"message" : "Create Product"}

csg_router.post("/create_gender")
async def create_gender(gender_input: Gender, session: Annotated[Session, Depends(get_session)]):
    # gender = await create_genders(gender_input,session)
    return {"message" : "Create Product"}

csg_router.get("/get_genders")
async def get_genders(category_input: Gender, session: Annotated[Session, Depends(get_session)]):
    # gender = await get_genders(gender_input, session)
    return {"message" : "Create Product"}