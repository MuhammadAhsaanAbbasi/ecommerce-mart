from ..schemas.user_emails import send_otp_notification_func, send_reset_password_notification_func
from fastapi import APIRouter, Depends, HTTPException
from ..utils.auth import get_current_active_user
from ..utils.auth import create_verify_token
from typing import Annotated, Optional, List
from ..core.config import verify_email_func
from ..model.authentication import Users
from ..utils.actions import generate_otp
from sqlmodel import select
from ..core.db import DB_SESSION

router = APIRouter(prefix="/api/v1/notification")

@router.post("/reset_password")
async def custom_notification(email: str):
    verify_user_token = create_verify_token(email)
    response = await send_reset_password_notification_func(user_email=email, subject="Reset Password Notification", token=verify_user_token)
    print(response)
    return response