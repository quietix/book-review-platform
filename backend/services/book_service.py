from typing import List

from sqlalchemy.orm import Session

from config import logger
from excepitons.isbn_api_exceptions import IsbnAPIException
from utils import isbn_api_utils

from schemas.book_schema import BookDetails, BookCreateByIsbn, BookAutomaticCreationByIsbn
from schemas.author_schema import AuthorCreate

from repositories.book_repository import BookRepository
from repositories.author_repository import AuthorRepository

from services.author_service import AuthorService


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
                            create_data: BookCreateByIsbn) -> BookDetails:
        scrapped_data = await isbn_api_utils.get_data_by_isbn(create_data.isbn)

        author_schema: AuthorCreate = await isbn_api_utils.scrap_author_data(scrapped_data)

        book_schema: BookAutomaticCreationByIsbn = (
            await isbn_api_utils.scrap_book_data(scrapped_data)
        )

        try:
            db_author = AuthorRepository.create_author_anonymously(session, author_schema)

            book_schema.author_id = db_author.id
            book_schema.isbn = create_data.isbn
            db_book = BookRepository.create_book_anonymously(session, book_schema)

            return db_book

        except Exception as e:
            exc = IsbnAPIException()
            logger.error(f"{exc.detail}. Details: {e}")
            raise exc
