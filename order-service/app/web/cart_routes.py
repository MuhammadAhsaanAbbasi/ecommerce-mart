from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from ..model.authentication import Users, Admin
from ..utils.admin_verify import get_current_active_admin_user
from ..utils.user_verify import get_current_active_user
from typing import Annotated, Optional, List
from ..core.db import DB_SESSION
import json

router = APIRouter(prefix="/api/v1")

@router.get("/create-cart")
async def create_carts(session: DB_SESSION, current_user: Annotated[Users, get_current_active_user]):
    return {"message" : "Order Services"}