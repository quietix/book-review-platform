from typing import Type

from sqlalchemy.orm import Session, joinedload

from config import logger
from models import (
    ReadingItem as ReadingItemModel,
    User as UserModel
)
from schemas.reading_item_schema import (
    ReadingItemCreate,
    ReadingItemUpdate
)

from exceptions.reading_item_exceptions import (
    ReadingItemDoesNotExist,
    CreateReadingItemException,
    DeleteReadingItemException
)


class ReadingItemRepository:
    @staticmethod
    def list_reading_items(session: Session,
                           authed_user: UserModel) -> list[Type[ReadingItemModel]]:
        return (
            session.query(ReadingItemModel)
            .filter(ReadingItemModel.user_id == authed_user.id)
            .order_by(ReadingItemModel.id)
            .all()
        )

    @staticmethod
    def list_reading_items_and_prefetch(session: Session,
                                        authed_user: UserModel) -> list[Type[ReadingItemModel]]:
        return session.query(ReadingItemModel).options(
            joinedload(ReadingItemModel.book),
            joinedload(ReadingItemModel.status)
        ).filter(
            ReadingItemModel.user_id == authed_user.id
        ).order_by(
            ReadingItemModel.id
        ).all()

    @staticmethod
    def retrieve_reading_item(session: Session,
                              reading_item_id: int,
                              authed_user: UserModel) -> Type[ReadingItemModel]:
        db_reading_item = (
            session.query(ReadingItemModel)
            .filter(
                ReadingItemModel.user_id == authed_user.id,
                ReadingItemModel.id == reading_item_id
            )
            .order_by(ReadingItemModel.id)
            .first()
        )

        if not db_reading_item:
            raise ReadingItemDoesNotExist()

        return db_reading_item

    @staticmethod
    def retrieve_reading_item_and_prefetch(session: Session,
                                           reading_item_id: int,
                                           authed_user: UserModel) -> Type[ReadingItemModel]:
        db_reading_item = (
            session.query(ReadingItemModel).options(
                joinedload(ReadingItemModel.book),
                joinedload(ReadingItemModel.status)
            ).filter(
                ReadingItemModel.user_id == authed_user.id,
                ReadingItemModel.id == reading_item_id
            ).order_by(
                ReadingItemModel.id
            ).first()
        )

        if not db_reading_item:
            raise ReadingItemDoesNotExist()

        return db_reading_item

    @staticmethod
    def filter_reading_item_by_book_and_user(session: Session,
                                             book_id: int,
                                             user_id: int) -> Type[ReadingItemModel]:
        db_reading_item = (
            session.query(ReadingItemModel)
            .filter(
                ReadingItemModel.book_id == book_id,
                ReadingItemModel.user_id == user_id
            )
            .first()
        )

        return db_reading_item

    @classmethod
    def create_reading_item(cls,
                            session: Session,
                            create_data: ReadingItemCreate,
                            authed_user: UserModel) -> ReadingItemModel:
        existing_reading_item = cls.filter_reading_item_by_book_and_user(
            session, create_data.book_id, authed_user.id
        )
        if existing_reading_item:
            exc = CreateReadingItemException(
                detail="You've already created Reading Item for this book."
            )
            logger.error(f"Error in ReadingItemRepository::create_reading_item. "
                         f"Details: {exc.detail}")
            raise exc

        try:
            db_status = ReadingItemModel(
                **create_data.model_dump(),
                user_id=authed_user.id
            )
            session.add(db_status)
            session.commit()
            return db_status

        except Exception as e:
            exc = CreateReadingItemException()
            logger.error(f"Error in ReadingItemRepository::create_reading_item. "
                         f"Details: {e}")
            raise exc

    @classmethod
    def partial_update_reading_item(cls,
                                    session: Session,
                                    reading_item_id: int,
                                    update_data: ReadingItemUpdate,
                                    authed_user: UserModel) -> Type[ReadingItemModel]:
        db_reading_item = cls.retrieve_reading_item(session, reading_item_id, authed_user)
        update_data = update_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_reading_item, key, value)

        try:
            session.commit()

        except Exception as e:
            exc = ReadingItemUpdate()
            logger.error(f"Error in ReadingItemRepository::partial_update_reading_item. "
                         f"Details: {e}")
            raise exc

        return db_reading_item

    @classmethod
    def delete_reading_item(cls,
                            session: Session,
                            reading_item_id: int,
                            authed_user: UserModel) -> bool:
        db_reading_item = cls.retrieve_reading_item(
            session, reading_item_id, authed_user
        )

        if not db_reading_item:
            raise ReadingItemDoesNotExist()

        try:
            session.delete(db_reading_item)
            session.commit()
            return True

        except Exception as e:
            exc = DeleteReadingItemException()
            logger.error(f"Error in ReadingItemRepository::delete_reading_item. "
                         f"{exc.detail}. Details: {e}")
            raise exc
