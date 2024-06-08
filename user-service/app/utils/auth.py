from ..setting import ALGORITHM, SECRET_KEY
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status
from ..core.db import get_session
from sqlmodel import select, Session
from typing import Annotated, Union
from ..model.models import Users, Token, TokenData, Admin, UserBase
from passlib.context import CryptContext
import resend # type: ignore 
import numpy as np

# Set your API key
resend.api_key = "re_K6Jhif6u_BVUGdYvzWjVjioaJR4Cpq28X"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = 3
REFRESH_TOKEN_EXPIRE_MINUTES = 5
def get_password_hash(password) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db, email: str | None, session: Annotated[Session, Depends(get_session)]):
    correct_user = session.exec(select(db).where(db.email == email)).first()
    if correct_user:
        return correct_user

def authenticate_user(db, email: str, password: str, session: Annotated[Session, Depends(get_session)]):
    user = get_user(db, email, session)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    else:
        return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if not isinstance(SECRET_KEY, str):
        raise ValueError("SECRET_KEY must be a string")

    if not isinstance(ALGORITHM, str):
            raise ValueError("ALGORITHM must be a string")
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Annotated[Session, Depends(get_session)]):
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
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(Users, email=token_data.email, session=session)
    if user is None:
        raise credentials_exception
    return user


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

async def get_current_admin(token: Annotated[str, Depends(oauth2_scheme)], session: Annotated[Session, Depends(get_session)]):
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
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(Admin, email=token_data.email, session=session)
    if user is None:
        raise credentials_exception
    return user

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


def validate_refresh_token(token: str, session: Annotated[Session, Depends(get_session)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: Union[str, None] = payload.get("email")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = session.exec(select(Users).where(Users.email == email)).first()
    if user is None:
        raise credentials_exception
    return user


async def tokens_service(refresh_token: str, session: Annotated[Session, Depends(get_session)]):
    user = validate_refresh_token(refresh_token, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    access_token_expires = timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    refresh_token_expires = timedelta(minutes=float(REFRESH_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_refresh_token(data={"email": user.email}, expires_delta=refresh_token_expires)
    print(ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "access_expires_in": int(access_token_expires.total_seconds()), 
        "refresh_token_expires_in": int(refresh_token_expires.total_seconds()),
        "refresh_token": refresh_token
    }


def generate_otp():
    """
    Generate a random OTP using numpy.
    """
    return ''.join(np.random.choice([str(i) for i in range(10)], size=6))


def generate_and_send_otp(user: UserBase, session: Session, user_id: int | None = None, image_url: str | None = None):
    # Generate OTP
    otp = generate_otp()
    print(otp)
    
    # hashed otp
    user.otp = get_password_hash(otp)
    user.hashed_password = get_password_hash(user.hashed_password)
    user.imageUrl = image_url
    normal_user = Users(**user.model_dump())
    session.add(normal_user)
    session.commit()
    session.refresh(normal_user)

    # Send OTP to user
    params = {
        "from": "onboarding@resend.dev",
        "to": ["mahsaanabbasi@gmail.com"],
        "subject": "Your OTP for sign-up",
        "html": f"<p>Your OTP is: {otp}</p>",
    }
    response = resend.Emails.send(params)
    print(response)