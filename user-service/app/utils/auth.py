from ..setting import ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, RESEND_API_KEY
from app.service.kong_consumer import create_consumer_in_kong, create_jwt_credentials_in_kong 
from ..model.models import Users, TokenData, Admin, UserBase, UserModel
from fastapi.security.oauth2 import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends, status
from jose import jwt, JWTError
from ..core.db import DB_SESSION
from sqlmodel import select, Session
from typing import Annotated, Union, Optional
from passlib.context import CryptContext
import resend # type: ignore 
import numpy as np
import json

# Set your API key
resend.api_key = RESEND_API_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash Value
def get_value_hash(password) -> str:
    return pwd_context.hash(password)

# verify Password
def verify_password(plain_password: str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Get User in db
def get_user(db, email: str | None, session: DB_SESSION):
    correct_user = session.exec(select(db).where(db.email == email)).first()
    if correct_user:
        return correct_user

# Authenticate the User
def authenticate_user(db, email: str, password: str, session: DB_SESSION):
    user = get_user(db, email, session)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    else:
        return user

# Create Access Token
def create_access_token(user: UserBase, expires_delta: Optional[Union[timedelta, None]] = None) -> str:
    if not isinstance(SECRET_KEY, str):
        raise ValueError("SECRET_KEY must be a string")
    if not isinstance(ALGORITHM, str):
        raise ValueError("ALGORITHM must be a string")
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    payload = {
        # "sub": user.email,
        "username": user.email,
        "iss": user.kid,  # Add issuer claim
        "exp": expire
    }

    headers = {
        "kid": user.kid
    }

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM, headers=headers)
    return encoded_jwt

# Get Current User
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: DB_SESSION):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: Union[str, None] = payload.get("username")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(Users, email=token_data.email, session=session)
    if user is None:
        raise credentials_exception
    return user

# Get Current Active & Verify User
async def get_current_active_user(current_user: Annotated[Users, Depends(get_current_user)]):
    if current_user.is_verified:
        print(current_user.id)
        return current_user
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Get Current Admin
async def get_current_admin(token: Annotated[str, Depends(oauth2_scheme)], session: DB_SESSION):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: Union[str, None] = payload.get("username")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(Admin, email=token_data.email, session=session)
    if user is None:
        raise credentials_exception
    return user

# Get Current Active & Verify Admin
async def get_current_active_admin_user(current_user: Annotated[Admin, Depends(get_current_admin)]):
    if current_user.is_verified:
        print(current_user.id)
        return current_user
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user or not an instructor",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Create Refresh Token
def create_refresh_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()

    if not isinstance(SECRET_KEY, str):
        raise ValueError("SECRET_KEY must be a string")

    if not isinstance(ALGORITHM, str):
            raise ValueError("ALGORITHM must be a string")
    
    # Convert UUID to string if it's present in the data
    if 'id' in to_encode and isinstance(to_encode['id'], int):
        to_encode['id'] = str(to_encode['id'])

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)  # Set the expiration time for refresh tokens to 7 days

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# Validate Refresh Token
def validate_refresh_token(db,token: str, session: DB_SESSION):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: Union[str, None] = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = session.exec(select(db).where(db.email == email)).first()
    if user is None:
        raise credentials_exception
    return user

# Token Service Function that Generate token
async def tokens_service(db, refresh_token: str, session: DB_SESSION):
    user = validate_refresh_token(db, refresh_token, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    access_token_expires = timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(user, expires_delta=access_token_expires)

    refresh_token_expires = timedelta(minutes=float(REFRESH_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_refresh_token(data={"sub": user.email}, expires_delta=refresh_token_expires)
    print(ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "access_expires_in": int(access_token_expires.total_seconds()), 
        "refresh_token_expires_in": int(refresh_token_expires.total_seconds()),
        "refresh_token": refresh_token
    }


# Generate Otp
def generate_otp():
    """
    Generate a random OTP using numpy.
    """
    return ''.join(np.random.choice([str(i) for i in range(10)], size=6))


# Generate & Send Otp
async def generate_and_send_otp(user: UserModel, session: Session, user_id: int | None = None, image_url: str | None = None):
    """
    Generate a random OTP using generate_otp function and that add some info of user in db and send a otp on the email.
    """
    # Generate OTP
    otp = generate_otp()
    print(otp)
    
    # hashed otp
    user_otp = get_value_hash(otp)
    user.hashed_password = get_value_hash(user.hashed_password)
    user.imageUrl = image_url
    normal_user = Users(**user.model_dump(), otp=user_otp)
    session.add(normal_user)
    session.commit()
    session.refresh(normal_user)

    try:
        create_consumer_in_kong(normal_user.email)
        create_jwt_credentials_in_kong(normal_user.email, str(normal_user.kid))
    except HTTPException as e:
            raise HTTPException(status_code=500, detail=f"Error creating JWT credentials in Kong: {e}")

    # Send OTP to user
    params = {
        "from": "onboarding@resend.dev",
        "to": ["mahsaanabbasi@gmail.com"],
        "subject": "Your OTP for sign-up",
        "html": f"<p>Your OTP is: {otp}</p>",
    }
    response = resend.Emails.send(params)
    print(response)

    # user_json  = dict(normal_user)
    return normal_user