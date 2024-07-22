from fastapi import APIRouter, Response, HTTPException, Request, Depends, Query
from ..utils.admin_verify import get_current_active_admin_user
from typing import Annotated, Optional, List, Sequence
from ..model.authentication import Users, Admin
from ..model.order import OrderMetadata, Order
from fastapi.responses import JSONResponse
from ..core.db import DB_SESSION
from datetime import datetime
from sqlmodel import select
import json


router = APIRouter(prefix="/api/v1/assistant")

@router.post("/order")
async def admin_assistant(session: DB_SESSION):
    return {"message" : "Assistant API Routes"}