from ..utils.auth import authenticate_user, create_access_token, create_refresh_token, generate_and_send_otp, get_value_hash
from app.service.kong_consumer import create_consumer_in_kong, create_jwt_credentials_in_kong 
from ..setting import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, USER_SIGNUP_EMAIL_TOPIC
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from aiokafka.errors import KafkaTimeoutError # type: ignore
from aiokafka import AIOKafkaProducer # type: ignore
from ..model.models import Users, Token, Admin, UserBase
from ..kafka.user_producer import get_kafka_producer
from fastapi import Depends, HTTPException, Form
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext
from typing import Annotated
from sqlmodel import select
from ..core.db import DB_SESSION
from datetime import timedelta
from app import user_pb2
import string
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Verify and Generate tokens
async def verify_and_generate_tokens(user_otp: str, user: Users, session: DB_SESSION, aio_producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    try:
        # Check if the user exists
        existing_user = session.exec(select(Users).where(Users.email == user.email)).first()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Verify OTP
        valid_otp = pwd_context.verify(user_otp, existing_user.otp)
        if not valid_otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")

        # Update is_verified field
        existing_user.is_verified = True
        session.commit()

        # Generate tokens
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(existing_user, expires_delta=access_token_expires)
        refresh_token_expires = timedelta(minutes=float(REFRESH_TOKEN_EXPIRE_MINUTES))
        refresh_token = create_refresh_token(data={"email": user.email}, expires_delta=refresh_token_expires)

        # Create protobuf message
        user_protobuf = user_pb2.EmailUser(
            username=user.username,
            email=user.email,
            imageUrl=user.imageUrl,
            is_active=user.is_active,
            is_verified=user.is_verified,
            role=user.role
        ) # type: ignore

        # Serialize the message to a byte string
        serialized_user = user_protobuf.SerializeToString()
        print(f"Serialized data: {serialized_user}")

        # Produce message to Kafka
        await aio_producer.send_and_wait(topic=USER_SIGNUP_EMAIL_TOPIC, value=serialized_user)
        print("Message sent to Kafka topic")

    except KafkaTimeoutError as e:
        print(f"Error in sending message to Kafka: {e}")
        raise HTTPException(status_code=500, detail="Error in sending message to Kafka")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    finally:
        await aio_producer.stop()

    # Return tokens
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "access_expires_in": int(access_token_expires.total_seconds()),
        "refresh_token_expires_in": int(refresh_token_expires.total_seconds()),
        "refresh_token": refresh_token,
    }

#  Create user 
async def create_user(user: Users, session: DB_SESSION, isGoogle: bool = False):
    existing_user = session.exec(select(Users).where(Users.email == user.email)).first()
    if existing_user:
        return False  # Return False if user already exists

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
def create_admin(user: Admin, session: DB_SESSION):
    is_verified = True
    existing_admin = session.exec(select(Admin).where(Admin.email == user.email)).first()
    if existing_admin:
            raise HTTPException(status_code=400, detail="Admin already exists")
    user.is_verified=is_verified
    user.hashed_password = get_value_hash(user.hashed_password)
    session.add(user)
    session.commit() 
    session.refresh(user)

    return {"message" : "Admin Created Successfully", "data": user}


#  Login for access Token
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    session: DB_SESSION
) -> Token:
    user = authenticate_user(Users, form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user, expires_delta=access_token_expires)
    refresh_token_expires = timedelta(minutes=float(REFRESH_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_refresh_token(data={"email": user.email}, expires_delta=refresh_token_expires)
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        access_expires_in=int(access_token_expires.total_seconds()),
        refresh_token_expires_in=int(refresh_token_expires.total_seconds()),
        refresh_token=refresh_token,
    )


# Login Access Token for Admin
async def login_access_token_for_admin(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: DB_SESSION)->Token:
    user = authenticate_user(Admin, form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user, expires_delta=access_token_expires
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
async def google_user(session: DB_SESSION, username:str, email:str, picture:str):
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
                    user, expires_delta=access_token_expires)
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

