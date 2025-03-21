from typing import List

from sqlalchemy.orm import Session

from config import logger
from excepitons.isbn_api_exceptions import IsbnAPIException
from utils import isbn_api_utils
from models import User as UserModel

from schemas.book_schema import (
    BookDetails,
    BookCreateByIsbn,
    BookCreateManually,
)
from schemas.author_schema import AuthorCreate

from repositories.book_repository import BookRepository
from repositories.author_repository import AuthorRepository


class BookService:
    @classmethod
    def list_books(cls, session: Session) -> List[BookDetails]:
        authors = BookRepository.list_books_and_prefetch(session)
        return [BookDetails.model_validate(author) for author in authors]

    @classmethod
    def retrieve_book(cls, session: Session, author_id: int) -> BookDetails:
        db_author = BookRepository.retrieve_books_and_prefetch(session, author_id)
        return BookDetails.model_validate(db_author)

    @classmethod
    async def create_book_by_isbn(cls,
                                  session: Session,
                                  authed_user: UserModel,
                                  create_data: BookCreateByIsbn) -> BookDetails:
        scrapped_data = await isbn_api_utils.get_data_by_isbn(create_data.isbn)
        author_schema: AuthorCreate = await isbn_api_utils.scrap_author_data(scrapped_data)
        book_schema = (
            await isbn_api_utils.scrap_book_data(scrapped_data)
        )

        try:
            db_author = AuthorRepository.get_or_create_author(session, author_schema, authed_user)
            logger.debug(f"db_author = {db_author}")

            book_schema.author_id = db_author.id
            book_schema.isbn = create_data.isbn
            book_schema = BookCreateManually(**book_schema.model_dump())

            db_book = BookRepository.create_book_manually(session, book_schema, authed_user)
            return db_book

        except Exception as e:
            exc = IsbnAPIException()
            logger.error(f"{exc.detail}. Details: {e}")
            raise exc
