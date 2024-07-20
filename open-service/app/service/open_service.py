from ..model.product import Product, ProductItem, ProductSize, Stock, SizeModel, ProductItemFormModel, ProductFormModel, Size
# from ..model.order import OrderModel, Order, OrderItem, OrderUpdateStatus, OrderItemMetadata, OrderMetadata, OrderStatus
from ..utils.admin_verify import get_current_active_admin_user
from ..utils.actions import all_product_details
from ..utils.user_verify import get_current_active_user
from fastapi import Depends, HTTPException, Query
from ..model.authentication import Users, Admin
from typing import Annotated, Optional, List, Sequence
from ..core.db import DB_SESSION
from datetime import datetime
from sqlmodel import select
import json
import uuid

async def get_all_product_details(session: DB_SESSION):
    products = session.exec(select(Product)).all()

    product_details = await all_product_details(products, session)

    return product_details