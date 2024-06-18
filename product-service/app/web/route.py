from fastapi import APIRouter, Depends,  Form, Request, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
# from ..service.auth import login_for_access_token, google_user, verify_and_generate_tokens
# from ..utils.auth import get_current_active_user, tokens_service, oauth2_scheme, get_current_user, get_value_hash
# from ..model.models import Users, Token, UserBase
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
router = APIRouter(prefix="/api/v1")

router.post("/create_product")
async def create_product():
    return {"message" : "Create Product"}