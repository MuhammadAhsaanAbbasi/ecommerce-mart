from ..model.product import Product, ProductItem, ProductSize, Stock, SizeModel, ProductItemFormModel, ProductFormModel
# from ..model.order 
from fastapi import Depends, UploadFile, File, Form, HTTPException
from ..utils.user_verify import get_current_active_user
from ..model.authentication import Users
from typing import Annotated, Optional, List
from ..core.db import DB_SESSION
from sqlmodel import select
import json
