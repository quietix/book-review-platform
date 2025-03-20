from typing import Type

from sqlalchemy.orm import Session

from config import logger
from models import Genre as GenreModel
from schemas.genre_schema import (
    GenreCreate,
    GenreUpdate,
)

from excepitons.genre_exceptions import (
    GenreDoesNotExist,
    CreateGenreException,
    UpdateGenreException,
    DeleteGenreException
)


class GenreRepository:
    @staticmethod
    def list_genres(session: Session) -> list[Type[GenreModel]]:
        return session.query(GenreModel).all()

    @staticmethod
    def retrieve_genre(session: Session, genre_id: int) -> Type[GenreModel]:
        db_genre = (session.query(GenreModel).filter(GenreModel.id == genre_id).first())

        if not db_genre:
            raise GenreDoesNotExist()

        return db_genre

    @classmethod
    def create_genre(cls,
                     session: Session,
                     create_data: GenreCreate) -> GenreModel:
        try:
            db_genre = GenreModel(**create_data.model_dump())
            session.add(db_genre)
            session.commit()
            return db_genre

        except Exception as e:
            exc = CreateGenreException()
            logger.error(f"{exc.detail}. Details: {e}")
            raise exc

    @classmethod
    def partial_update_genre(cls,
                             session: Session,
                             author_id: int,
                             update_data: GenreUpdate) -> Type[GenreModel]:
        db_author = cls.retrieve_genre(session, author_id)
        update_data = update_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_author, key, value)

        try:
            session.commit()

        except Exception as e:
            exc = UpdateGenreException()
            logger.error(f"{exc.detail}. Details: {e}")
            raise exc

        return db_author

    @classmethod
    def delete_genre(cls, session: Session, author_id: int) -> bool:
        db_author = cls.retrieve_genre(session, author_id)

        if not db_author:
            raise GenreDoesNotExist()

        try:
            session.delete(db_author)
            session.commit()
            return True

        except Exception as e:
            exc = DeleteGenreException()
            logger.error(f"{exc.detail}. Details: {e}")
            raise exc
