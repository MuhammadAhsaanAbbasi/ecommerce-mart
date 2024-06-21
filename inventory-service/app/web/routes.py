from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from typing import Annotated, Optional, List
from ..core.db import DB_SESSION
from sqlmodel import Session
import json

router = APIRouter(prefix="/api/v1")

@router.get("/inventory")
async def inventory(session: DB_SESSION):
    return {"message" : "Inventory Services"}