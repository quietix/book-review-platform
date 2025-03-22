from typing import Type, Optional

from sqlalchemy.orm import Session, joinedload

from config import logger
from models import (
    Author as AuthorModel,
    User as UserModel,
)
from schemas.author_schema import (
    AuthorPartialUpdate,
    AuthorCreate,
)
from excepitons.author_exceptions import (
    AuthorDoesNotExist,
    CreateAuthorException,
    UpdateAuthorException,
    DeleteAuthorException
)


class AuthorRepository:
    @staticmethod
    def list_authors(session: Session) -> list[Type[AuthorModel]]:
        return session.query(AuthorModel).order_by(AuthorModel.id).all()

    @staticmethod
    def retrieve_author(session: Session, author_id: int) -> Type[AuthorModel]:
        db_author = (session.query(AuthorModel).filter(AuthorModel.id == author_id).first())

        if not db_author:
            raise AuthorDoesNotExist()

        return db_author

    @staticmethod
    def retrieve_author_by_name_surname(session: Session,
                                        author_name: str,
                                        author_surname: str) -> Optional[Type[AuthorModel]]:
        db_author = (session.query(AuthorModel).filter(
            AuthorModel.name == author_name,
            AuthorModel.surname == author_surname
        ).first())

        return db_author

    @staticmethod
    def list_authors_and_prefetch(session: Session) -> list[Type[AuthorModel]]:
        return session.query(AuthorModel).options(joinedload(AuthorModel.publisher)).all()

    @staticmethod
    def retrieve_author_and_prefetch(session: Session, author_id: int) -> Type[AuthorModel]:
        db_author = (session.query(AuthorModel).options(joinedload(AuthorModel.publisher))
                     .filter(AuthorModel.id == author_id).first())

        if not db_author:
            raise AuthorDoesNotExist()

        return db_author

    @classmethod
    def create_author(cls,
                      session: Session,
                      create_data: AuthorCreate,
                      authed_user: UserModel) -> AuthorModel:
        try:
            db_author = AuthorModel(**create_data.model_dump(), publisher_id=authed_user.id)
            session.add(db_author)
            session.commit()
            return db_author

        except Exception as e:
            logger.error(f"Failed to create the author. Details: {e}")
            raise CreateAuthorException()

    @classmethod
    def get_or_create_author(cls,
                             session: Session,
                             create_data: AuthorCreate,
                             authed_user: UserModel) -> AuthorModel:
        db_author = cls.retrieve_author_by_name_surname(
            session,
            author_name=create_data.name,
            author_surname=create_data.surname
        )

        if db_author:
            return db_author

        try:
            db_author = AuthorModel(**create_data.model_dump(), publisher_id=authed_user.id)
            session.add(db_author)
            session.commit()
            return db_author

        except Exception as e:
            logger.error(f"Failed to create the author. Details: {e}")
            raise CreateAuthorException()

    @classmethod
    def partial_update_author(cls,
                              session: Session,
                              author_id: int,
                              update_data: AuthorPartialUpdate) -> Type[AuthorModel]:
        db_author = cls.retrieve_author(session, author_id)
        update_data = update_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_author, key, value)

        try:
            session.commit()

        except Exception as e:
            logger.error(f"Failed to update the author. Details: {e}")
            raise UpdateAuthorException()

        return db_author

    @classmethod
    def delete_author(cls, session: Session, author_id: int) -> bool:
        db_author = cls.retrieve_author(session, author_id)

        if not db_author:
            raise AuthorDoesNotExist()

        try:
            session.delete(db_author)
            session.commit()
            return True

        except Exception as e:
            logger.error(f"Failed to delete author. Details: {e}")
            raise DeleteAuthorException()
