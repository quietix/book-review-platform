from typing import Type

from sqlalchemy.orm import Session, joinedload

from config import logger

from models import (
    User as UserModel,
    Rating as RatingModel,
)
from schemas.rating_schema import (
    RatingCreate,
    RatingUpdate,
)
from exceptions.rating_exceptions import (
    RatingDoesNotExist,
    CreateRatingException,
    UpdateRatingException,
    DeleteRatingException
)


class RatingRepository:
    @staticmethod
    def list_ratings(session: Session) -> list[Type[RatingModel]]:
        return session.query(RatingModel).order_by(RatingModel.id).all()

    @staticmethod
    def retrieve_rating(session: Session, rating_id: int) -> Type[RatingModel]:
        db_rating = (session.query(RatingModel).filter(RatingModel.id == rating_id).first())

        if not db_rating:
            raise RatingDoesNotExist()

        return db_rating

    @staticmethod
    def retrieve_rating_by_book_and_user(session: Session, book_id: int, user_id: int):
        db_rating = (session.query(RatingModel).filter(
            RatingModel.book_id == book_id,
            RatingModel.user_id == user_id
        ).first())

        if not db_rating:
            raise RatingDoesNotExist()

        return db_rating

    @staticmethod
    def list_ratings_and_prefetch(session: Session) -> list[Type[RatingModel]]:
        return session.query(RatingModel).options(
            joinedload(RatingModel.book),
            joinedload(RatingModel.user)
        ).all()

    @staticmethod
    def retrieve_ratings_and_prefetch(session: Session, rating_id: int) -> Type[RatingModel]:
        db_rating = (session.query(RatingModel).options(
            joinedload(RatingModel.book),
            joinedload(RatingModel.user)
        ).filter(RatingModel.id == rating_id).first())

        if not db_rating:
            raise RatingDoesNotExist()

        return db_rating

    @staticmethod
    def is_book_rated_by_the_user(session: Session,
                                  book_id: int,
                                  user_id: int) -> bool:
        rating_exists = session.query(RatingModel).filter(
            RatingModel.user_id == user_id,
            RatingModel.book_id == book_id
        ).first()

        return rating_exists is not None

    @classmethod
    def create_rating(cls,
                      session: Session,
                      create_data: RatingCreate,
                      authed_user: UserModel) -> RatingModel:
        if create_data.rating not in range(1, 6):
            exc = CreateRatingException(detail="Rating must be bigger than 1 and less than 6.")
            logger.error(f"Error in RatingRepository::create_rating. Details: {exc.detail}")
            raise exc

        if cls.is_book_rated_by_the_user(session, create_data.book_id, authed_user.id):
            exc = CreateRatingException(detail="This book is already rated by this user.")
            logger.error(f"Error in RatingRepository::create_rating. Details: {exc.detail}")
            raise exc

        try:
            db_rating = RatingModel(
                **create_data.model_dump(),
                user_id=authed_user.id
            )
            session.add(db_rating)
            session.commit()
            return db_rating

        except Exception as e:
            exc = CreateRatingException()
            logger.error(f"Error in RatingRepository::create_rating. {exc.detail}. Details: {e}")
            raise exc

    @classmethod
    def partial_update_rating(cls,
                              session: Session,
                              rating_id: int,
                              update_data: RatingUpdate) -> Type[RatingModel]:
        if update_data.rating and update_data.rating not in range(1, 6):
            exc = CreateRatingException(detail="Rating must be bigger than 1 and less than 6.")
            logger.error(f"Error in RatingRepository::create_rating. Details: {exc.detail}")
            raise exc

        db_rating = cls.retrieve_rating(session, rating_id)
        update_data = update_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_rating, key, value)

        try:
            session.commit()

        except Exception as e:
            exc = UpdateRatingException()
            logger.error(f"Error in RatingRepository::partial_update_rating. "
                         f"{exc.detail}. Details: {e}")
            raise exc

        return db_rating

    @classmethod
    def delete_rating(cls, session: Session, rating_id: int) -> bool:
        db_rating = cls.retrieve_rating(session, rating_id)

        if not db_rating:
            raise RatingDoesNotExist()

        try:
            session.delete(db_rating)
            session.commit()
            return True

        except Exception as e:
            exc = DeleteRatingException()
            logger.error(f"Error in RatingRepository::delete_rating. "
                         f"{exc.detail}. Details: {e}")
            raise exc
