from typing import Type

from sqlalchemy.orm import Session, joinedload

from config import logger

from models import (
    Author as AuthorModel,
    User as UserModel,
    Book as BookModel,
)
from schemas.book_schema import (
    BookCreateManually,
    BookPartialUpdate,
    BookAutomaticCreationByIsbn,
)
from excepitons.book_exceptions import (
    BookDoesNotExist,
    CreateBookException,
    UpdateBookException,
    DeleteBookException
)


class BookRepository:
    @staticmethod
    def list_books(session: Session) -> list[Type[BookModel]]:
        return session.query(BookModel).all()

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
    def create_book_anonymously(cls,
                                session: Session,
                                create_data: BookAutomaticCreationByIsbn) -> AuthorModel:
        try:
            db_book = BookModel(**create_data.model_dump(exclude_unset=True))
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
