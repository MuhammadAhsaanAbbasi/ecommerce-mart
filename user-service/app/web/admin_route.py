from fastapi import APIRouter, Depends,  Form, Request, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse, Response
from ..service.auth import create_admin, login_access_token_for_admin
from ..utils.auth import get_current_active_admin_user
from ..model.models import Users, Token, Admin
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

# admin routes
@admin_router.get("/profile", response_model=Admin)
async def read_users_admin(current_user: Annotated[Admin, Depends(get_current_active_admin_user)]):
    return current_user