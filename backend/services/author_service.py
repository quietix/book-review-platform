from typing import List

from sqlalchemy.orm import Session

from repositories.author_repository import AuthorRepository
from schemas.author_schema import AuthorDetails


class AuthorService:

    @classmethod
    def list_authors(cls, session: Session) -> List[AuthorDetails]:
        authors = AuthorRepository.list_authors_and_prefetch(session)
        return [AuthorDetails.model_validate(author) for author in authors]

    @classmethod
    def retrieve_author(cls, session: Session, author_id: int) -> AuthorDetails:
        db_author = AuthorRepository.retrieve_author_and_prefetch(session, author_id)
        return AuthorDetails.model_validate(db_author)
