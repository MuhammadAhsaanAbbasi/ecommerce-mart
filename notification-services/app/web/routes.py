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

router = APIRouter(prefix="/api/v1")

@router.get("/custom-notifications")
async def custom_notification(
                            session: DB_SESSION,
                            current_user: Annotated[Users, Depends(get_current_active_user)],
                            otp_email: bool = False,
                            ):
    verify_user_token = create_verify_token(current_user.email)
    if otp_email:
        otp = generate_otp()

        existing_user = session.exec(select(Users).where(Users.email == current_user.email)).first()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        existing_user.otp = otp
        session.commit()
        session.refresh(existing_user)

        response = await send_otp_notification_func(user_email=current_user.email, subject="OTP Notification", token=verify_user_token, otp="89344")
        return response
    else:
        response = await send_reset_password_notification_func(user_email=current_user.email, subject="Reset Password Notification", token=verify_user_token)
        return response