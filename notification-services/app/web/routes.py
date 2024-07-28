from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from typing import Annotated, Optional, List
from ..core.config import is_email_verified, verify_email_func
from ..utils.actions import send_custom_notification_func
from ..core.db import DB_SESSION
from sqlmodel import Session
import json

router = APIRouter(prefix="/api/v1")

@router.get("/custom-notifications")
async def custom_notification(user_email: str):
    if not is_email_verified(user_email):
        verify_email_func(email_address=user_email)
        return {"message": "Verification Email sent! Please verify your email address to receive notifications."}
    else:
        response = await send_custom_notification_func(user_email, "OTP Notification", f"This is a OTP notification, OTP is {7789}")
        return response