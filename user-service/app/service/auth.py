from ..utils.auth import authenticate_user, create_access_token, create_refresh_token, generate_and_send_otp, REFRESH_TOKEN_EXPIRE_MINUTES, ACCESS_TOKEN_EXPIRE_MINUTES
from app.service.kong_consumer import create_consumer_in_kong, create_jwt_credentials_in_kong 
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..model.models import Users, Token, Admin, UserBase
from fastapi import Depends, HTTPException, Form
from fastapi.responses import RedirectResponse
from typing import Annotated, Optional
from sqlmodel import  Session, select
from ..core.db import get_session
from datetime import timedelta
import string
import secrets
import resend # type: ignore
import numpy as np
# Set your API key 
resend.api_key = "re_K6Jhif6u_BVUGdYvzWjVjioaJR4Cpq28X"
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Verify and Generate tokens
def verify_and_generate_tokens(user_otp: str, user: Users, session: Session):
    # Check if the user is an admin or a normal user
    # Verify OTP
    existing_user = session.exec(select(Users).where(Users.email == user.email)).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    valid_otp = pwd_context.verify(user_otp, existing_user.otp)
    if not valid_otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # If OTP is valid, update is_verified field
    existing_user.is_verified = True
    session.commit()

    # Return tokens
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    refresh_token_expires = timedelta(minutes=float(REFRESH_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_refresh_token(data={"email": user.email}, expires_delta=refresh_token_expires)

    return Token(
        access_token=access_token,
        token_type="bearer",
        access_expires_in=int(access_token_expires.total_seconds()),
        refresh_token_expires_in=int(refresh_token_expires.total_seconds()),
        refresh_token=refresh_token,
    )


#  Create user 
def create_user(user: Users, session: Annotated[Session, Depends(get_session)], isGoogle: bool = False):

    if isGoogle:
        user.is_verified = True
        session.add(user)
        session.commit()
        session.refresh(user)
        try:
            create_consumer_in_kong(user.email)
            create_jwt_credentials_in_kong(user.email, str(user.kid))
        except HTTPException as e:
            raise HTTPException(status_code=500, detail=f"Error creating JWT credentials in Kong: {e}")
        return {"detail": "User created successfully"}

    data = generate_and_send_otp(user, session)

    return {"detail": "OTP sent successfully"}


# Create Admin 
def create_admin(user: Admin, session: Annotated[Session, Depends(get_session)]):
    is_verified = True
    existing_admin = session.exec(select(Admin).where(Admin.email == user.email)).first()
    if existing_admin:
            raise HTTPException(status_code=400, detail="Admin already exists")
    user.is_verified=is_verified
    session.add(user)
    session.commit()
    session.refresh(user)

    return {"message" : "Admin Created Successfully", "data": user}


#  Login for access Token
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Annotated[Session, Depends(get_session)])->Token:
    user = authenticate_user(Users, form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(minutes=float(REFRESH_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_refresh_token(data={"email": user.email}, expires_delta=refresh_token_expires)
    print(ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=access_token, 
        token_type="bearer", 
        access_expires_in= int(access_token_expires.total_seconds()), 
        refresh_token_expires_in= int(refresh_token_expires.total_seconds()),
        refresh_token=refresh_token,
        )


# Login Access Token for Admin
async def login_access_token_for_admin(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Annotated[Session, Depends(get_session)])->Token:
    user = authenticate_user(Admin, form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

        # Generate refresh token (you might want to set a longer expiry for this)
    refresh_token_expires = timedelta(minutes=float(REFRESH_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_refresh_token(data={"email": user.email}, expires_delta=refresh_token_expires)
    print(ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=access_token, 
        token_type="bearer", 
        access_expires_in= int(access_token_expires.total_seconds()), 
        refresh_token_expires_in= int(refresh_token_expires.total_seconds()),
        refresh_token=refresh_token,
        )


# Google user Auth
async def google_user(session: Annotated[Session, Depends(get_session)], username:str, email:str, picture:str):
    user = session.exec(select(Users).where(Users.email == email)).first()
    try:
        if user is None:
            password_length = 12  # You can choose the length of the password
            characters = string.ascii_letters + string.digits + string.punctuation
            random_password = ''.join(secrets.choice(characters) for i in range(password_length))
            user_data = Users(username=username, email=email, hashed_password=random_password, imageUrl=picture)
            
            new_user = create_user(user_data, session, isGoogle=True)
            return new_user

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
                    data={"sub": user.username}, expires_delta=access_token_expires)
        print(f"access_token {access_token_expires.total_seconds()}")
        
        refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        refresh_token = create_refresh_token(
                    data={"sub": user.email}, expires_delta=refresh_token_expires)
        print(f"refresh_token {refresh_token_expires.total_seconds()}")
        
        response = RedirectResponse(url='http://localhost:3000/user/me')
        response.set_cookie(key="access_token", value=access_token, httponly=True, expires=int(access_token_expires.total_seconds()))
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, expires=int(refresh_token_expires.total_seconds()))

        return response
    except HTTPException as e:
        # Re-raise the exception to be handled in the web layer
        raise e
    except Exception as e:
        # Re-raise general exceptions to be handled in the web layer
        raise e

