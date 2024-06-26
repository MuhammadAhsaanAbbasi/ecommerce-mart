from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from typing import Annotated, Optional, List
from ..core.db import DB_SESSION
from sqlmodel import Session
import json

order_router = APIRouter(prefix="/api/v1")

@order_router.get("/order-service")
async def inventory(session: DB_SESSION):
    return {"message" : "Order Services"}