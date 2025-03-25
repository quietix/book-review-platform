from typing import Type

from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import func

from config import logger, config

from models import (
    Author as AuthorModel,
    User as UserModel,
    Book as BookModel,
    ReadingItem as ReadingItemModel,
    Rating as RatingModel,
    Status as StatusModel,
)
from schemas.book_schema import (
    BookCreateManually,
    BookPartialUpdate,
)
from exceptions.book_exceptions import (
    BookDoesNotExist,
    CreateBookException,
    UpdateBookException,
    DeleteBookException
)


class BookRepository:
    @staticmethod
    def list_books(session: Session) -> list[Type[BookModel]]:
        return session.query(BookModel).order_by(BookModel.id).all()

    @staticmethod
    def retrieve_book(session: Session, book_id: int) -> Type[BookModel]:
        db_book = (session.query(BookModel).filter(BookModel.id == book_id).first())

        if not db_book:
            raise BookDoesNotExist()

        return db_book

    @staticmethod
    def list_books_and_prefetch(session: Session) -> list[Type[BookModel]]:
        return session.query(BookModel).options(
            joinedload(BookModel.author),
            joinedload(BookModel.publisher),
            joinedload(BookModel.genre)
        ).all()

    @staticmethod
    def retrieve_books_and_prefetch(session: Session, book_id: int) -> Type[BookModel]:
        db_book = (session.query(BookModel).options(
            joinedload(BookModel.author),
            joinedload(BookModel.publisher),
            joinedload(BookModel.genre)
        ).filter(BookModel.id == book_id).first())

        if not db_book:
            raise BookDoesNotExist()

        return db_book

    @classmethod
    def create_book_manually(cls,
                             session: Session,
                             create_data: BookCreateManually,
                             authed_user: UserModel) -> AuthorModel:
        try:
            db_book = BookModel(
                **create_data.model_dump(exclude_unset=True),
                publisher_id=authed_user.id
            )
            session.add(db_book)
            session.commit()
            return db_book

        except Exception as e:
            exc = CreateBookException()
            logger.error(f"{exc.detail}. Details: {e}")
            raise exc

    @classmethod
    def partial_update_book(cls,
                            session: Session,
                            book_id: int,
                            update_data: BookPartialUpdate) -> Type[AuthorModel]:
        db_book = cls.retrieve_book(session, book_id)
        update_data = update_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_book, key, value)

        try:
            session.commit()

        except Exception as e:
            exc = UpdateBookException()
            logger.error(f"{exc.detail}. Details: {e}")
            raise exc

        return db_book

    @classmethod
    def delete_book(cls, session: Session, book_id: int) -> bool:
        db_book = cls.retrieve_book(session, book_id)

        if not db_book:
            raise BookDoesNotExist()

        try:
            session.delete(db_book)
            session.commit()
            return True

        except Exception as e:
            exc = DeleteBookException()
            logger.error(f"{exc.detail}. Details: {e}")
            raise exc

    @classmethod
    def get_recommendations(cls, session: Session, authed_user: UserModel):
        most_recent_author_subquery = (
            session.query(BookModel.author_id)
            .join(ReadingItemModel, ReadingItemModel.book_id == BookModel.id)
            .join(StatusModel, StatusModel.id == ReadingItemModel.status_id)
            .filter(
                ReadingItemModel.user_id == authed_user.id,
                StatusModel.status == config.FINISHED_BOOKS_STATUS_NAME
            )
            .order_by(ReadingItemModel.updated_at.desc())
            .limit(1)
            .subquery()
        )

        finished_books_subquery = (
            session.query(BookModel.id)
            .join(ReadingItemModel, ReadingItemModel.book_id == BookModel.id)
            .join(StatusModel, StatusModel.id == ReadingItemModel.status_id)
            .filter(
                ReadingItemModel.user_id == authed_user.id,
                StatusModel.status == config.FINISHED_BOOKS_STATUS_NAME
            )
            .subquery()
        )

        books_to_recommend = (
            session.query(
                BookModel
            )
            .join(RatingModel, RatingModel.book_id == BookModel.id, isouter=True)
            .filter(
                BookModel.author_id == most_recent_author_subquery.c.author_id,
                ~BookModel.id.in_(session.query(finished_books_subquery.c.id))
            )
            .group_by(BookModel.id)
            .order_by(func.coalesce(func.avg(RatingModel.rating), 0).desc())
            .all()
        )

        return books_to_recommend
