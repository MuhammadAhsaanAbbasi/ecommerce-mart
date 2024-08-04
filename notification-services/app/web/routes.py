from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from typing import Annotated, Optional, List
from ..core.config import verify_email_func
from ..utils.actions import send_otp_notification_func
from ..core.db import DB_SESSION
from sqlmodel import Session
import json

router = APIRouter(prefix="/api/v1")

@router.get("/custom-notifications")
async def custom_notification(user_email: str):
    response = await send_otp_notification_func(user_email=user_email, subject="OTP Notification", token=f"This is a OTP notification,", otp="89344")
    return response