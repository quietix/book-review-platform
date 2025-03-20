from typing import List

from sqlalchemy.orm import Session

from repositories.book_repository import BookRepository
from schemas.book_schema import BookDetails


class BookService:

    @classmethod
    def list_books(cls, session: Session) -> List[BookDetails]:
        authors = BookRepository.list_books_and_prefetch(session)
        return [BookDetails.model_validate(author) for author in authors]

    @classmethod
    def retrieve_book(cls, session: Session, author_id: int) -> BookDetails:
        db_author = BookRepository.retrieve_books_and_prefetch(session, author_id)
        return BookDetails.model_validate(db_author)
