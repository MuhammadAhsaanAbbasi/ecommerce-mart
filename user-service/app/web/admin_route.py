from fastapi import APIRouter, Depends,  Form, Request, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse, Response
from ..service.auth import create_admin, login_access_token_for_admin
from ..utils.auth import get_current_active_admin_user, tokens_service, oauth2_scheme, get_current_admin, get_value_hash
from ..model.models import Users, Token, Admin, UserBase
from typing import Annotated, Any, Optional
from sqlmodel import Session, select
from ..core.db import get_session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


admin_router = APIRouter(prefix="/api/v1/admin")

# Create Admin Routes
@admin_router.post("/create")
async def sign_up_admin(admin: Admin, session: Annotated[Session, Depends(get_session)]):
    admin = create_admin(admin, session)
    return admin


@admin_router.post("/login", response_model=Token)
async def login_access_token_admin(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Annotated[Session, Depends(get_session)]):
    token = await login_access_token_for_admin(form_data, session)
    return token

# token route
@admin_router.post("/admin/refresh_token", response_model=Token)
async def get_tokens(session: Annotated[Session, Depends(get_session)], refresh_token:Annotated[str, Depends(oauth2_scheme)]): 
    tokens = await tokens_service(db=Admin, refresh_token=refresh_token, session=session)
    return tokens


# admin routes
@admin_router.get("/profile", response_model=Admin)
async def read_users_admin(current_user: Annotated[Admin, Depends(get_current_active_admin_user)]):
    return current_user

@admin_router.put("/admin/reset-password")
async def reset_password(reset_password:str, current_user: Annotated[Admin, Depends(get_current_admin)], session:Annotated[Session, Depends(get_session)]):
    if current_user:
        current_user.hashed_password = get_value_hash(reset_password)
        session.commit()
        session.refresh(current_user)
        return {"message" : "Password Reset Successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid User Details & Credentials Token",
            headers={"WWW-Authenticate": "Bearer"},
        )

@admin_router.put("/admin/update")
async def update_user(current_user: Annotated[Admin, Depends(get_current_active_admin_user)], user:UserBase, session:Annotated[Session, Depends(get_session)]):
    if current_user:
        current_user.username = user.username
        current_user.imageUrl = user.imageUrl
        session.commit()
        session.refresh(current_user)
        return current_user
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid User Details & Credentials Token",
            headers={"WWW-Authenticate": "Bearer"},
        )