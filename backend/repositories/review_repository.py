from typing import Type

from sqlalchemy.orm import Session, joinedload

from config import logger
from repositories.rating_repository import RatingRepository
from schemas.rating_schema import RatingCreate
from schemas.review_schema import (
    ReviewCreate,
    ReviewUpdate
)
from models import (
    User as UserModel,
    Review as ReviewModel,
)
from exceptions.review_exceptions import (
    ReviewDoesNotExist,
    CreateReviewException,
    UpdateReviewException,
    DeleteReviewException
)


class ReviewRepository:
    @staticmethod
    def list_reviews(session: Session) -> list[Type[ReviewModel]]:
        return session.query(ReviewModel).order_by(ReviewModel.id).all()

    @staticmethod
    def retrieve_review(session: Session, review_id: int) -> Type[ReviewModel]:
        db_review = (session.query(ReviewModel).filter(ReviewModel.id == review_id).first())

        if not db_review:
            raise ReviewDoesNotExist()

        return db_review

    @staticmethod
    def filter_review_by_book_and_user(session: Session,
                                       book_id: int,
                                       user_id: int) -> Type[ReviewModel]:
        db_review = session.query(ReviewModel).filter(
            ReviewModel.book_id == book_id,
            ReviewModel.publisher_id == user_id
        ).first()

        return db_review

    @staticmethod
    def list_reviews_and_prefetch(session: Session) -> list[Type[ReviewModel]]:
        return session.query(ReviewModel).options(
            joinedload(ReviewModel.publisher),
            joinedload(ReviewModel.book),
            joinedload(ReviewModel.rating)
        ).all()

    @staticmethod
    def retrieve_reviews_and_prefetch(session: Session, review_id: int) -> Type[ReviewModel]:
        db_review = (session.query(ReviewModel).options(
            joinedload(ReviewModel.publisher),
            joinedload(ReviewModel.book),
            joinedload(ReviewModel.rating)
        ).filter(ReviewModel.id == review_id).first())

        if not db_review:
            raise ReviewDoesNotExist()

        return db_review

    @classmethod
    def create_review(cls,
                      session: Session,
                      create_data: ReviewCreate,
                      authed_user: UserModel) -> ReviewModel:
        existing_review = cls.filter_review_by_book_and_user(
            session, create_data.book_id, authed_user.id
        )
        if existing_review:
            exc = CreateReviewException(detail="You've already created review for this book.")
            logger.error(f"Error in ReviewRepository::create_review. Details: {exc.detail}")
            raise exc

        if create_data.rating:
            create_rating_data = RatingCreate(
                book_id=create_data.book_id, rating=create_data.rating
            )
            db_rating = RatingRepository.create_rating(session, create_rating_data, authed_user)
        else:
            db_rating = RatingRepository.retrieve_rating_by_book_and_user(
                session, create_data.book_id, authed_user.id
            )

        try:
            db_review = ReviewModel(
                **create_data.model_dump(exclude={"rating"}),
                publisher_id=authed_user.id,
                rating_id=db_rating.id,
            )
            session.add(db_review)
            session.commit()
            return db_review

        except Exception as e:
            exc = CreateReviewException()
            logger.error(f"Error in ReviewRepository::create_review. {exc.detail}. Details: {e}")
            raise exc

    @classmethod
    def partial_update_review(cls,
                              session: Session,
                              review_id: int,
                              update_data: ReviewUpdate) -> Type[ReviewModel]:
        db_review = cls.retrieve_review(session, review_id)
        update_data = update_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_review, key, value)

        try:
            session.commit()

        except Exception as e:
            exc = UpdateReviewException()
            logger.error(f"{exc.detail}. Details: {e}")
            raise exc

        return db_review

    @classmethod
    def delete_review(cls, session: Session, review_id: int) -> bool:
        db_review = cls.retrieve_review(session, review_id)

        if not db_review:
            raise ReviewDoesNotExist()

        try:
            session.delete(db_review)
            session.commit()
            return True

        except Exception as e:
            exc = DeleteReviewException()
            logger.error(f"{exc.detail}. Details: {e}")
            raise exc
