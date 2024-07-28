from ..utils.action import create_review, get_product_reviews_details, get_user_reviews_details
from ..utils.user_verify import get_current_active_user
from aiokafka import AIOKafkaProducer # type: ignore
from typing import Annotated, Optional, List, Dict
from ..model.authentication import Admin, Users
from ..kafka.producer import get_kafka_producer
from fastapi.responses import ORJSONResponse
from ..model.models import ReviewModel
from fastapi import APIRouter, Depends
from ..core.db import DB_SESSION


review_routes = APIRouter(prefix="/api/v1/reviews")


@review_routes.post('/create')
async def create_reviews(session: DB_SESSION,
                        review_details: ReviewModel,
                        current_user: Annotated[Users, Depends(get_current_active_user)]
                        ):
    review = await create_review(session, review_details, current_user)
    return ORJSONResponse({"message" : "Review created successfully", "review" : review})

@review_routes.get("/get_product_reviews/{product_id}")
async def get_product_reviews(product_id: str, session: DB_SESSION):
    reviews = await get_product_reviews_details(product_id, session)
    return reviews

@review_routes.get('/get_user_reviews')
async def get_user_reviews(session: DB_SESSION,
                        current_user: Annotated[Users, Depends(get_current_active_user)]
                        ):
    reviews = await get_user_reviews_details(session, current_user)
    return reviews