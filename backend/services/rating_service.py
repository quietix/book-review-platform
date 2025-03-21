import asyncio
from typing import List

from sqlalchemy.orm import Session

from config import logger
from excepitons.isbn_api_exceptions import IsbnAPIException
from utils import isbn_api_utils
from models import User as UserModel
from schemas.rating_schema import RatingDetails
from repositories.rating_repository import RatingRepository


class RatingService:
    @classmethod
    async def list_ratings(cls, session: Session) -> List[RatingDetails]:
        ratings = await asyncio.to_thread(RatingRepository.list_ratings_and_prefetch, session)
        return [RatingDetails.model_validate(rating) for rating in ratings]

    @classmethod
    async def retrieve_rating(cls, session: Session, rating_id: int) -> RatingDetails:
        db_rating = await asyncio.to_thread(
            RatingRepository.retrieve_ratings_and_prefetch, session, rating_id
        )
        return RatingDetails.model_validate(db_rating)
