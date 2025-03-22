import asyncio
from typing import List

from sqlalchemy.orm import Session

from schemas.review_schema import ReviewDetails
from repositories.review_repository import ReviewRepository


class ReviewService:
    @classmethod
    async def list_reviews(cls, session: Session) -> List[ReviewDetails]:
        reviews = await asyncio.to_thread(ReviewRepository.list_reviews_and_prefetch, session)
        return [ReviewDetails.model_validate(review) for review in reviews]

    @classmethod
    async def retrieve_review(cls, session: Session, review_id: int) -> ReviewDetails:
        db_review = await asyncio.to_thread(
            ReviewRepository.retrieve_reviews_and_prefetch, session, review_id
        )
        return ReviewDetails.model_validate(db_review)
