from ..setting import ALGORITHM, SECRET_KEY
from ..model.authentication import Token, TokenData, Users
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status
from jose import jwt, JWTError
from ..core.db import DB_SESSION
from typing import Annotated, Union, Optional
from .admin_verify import get_user
import json

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
    if current_user.is_active:
        print(current_user.id)
        return current_user
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )