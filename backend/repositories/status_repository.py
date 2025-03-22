from typing import Type

from sqlalchemy.orm import Session

from config import logger
from models import Status as StatusModel
from schemas.status_schema import StatusUpsert

from excepitons.status_exceptions import (
    StatusDoesNotExist,
    CreateStatusException,
    UpdateStatusException,
    DeleteStatusException
)


class StatusRepository:
    @staticmethod
    def list_statuses(session: Session) -> list[Type[StatusModel]]:
        return session.query(StatusModel).order_by(StatusModel.id).all()

    @staticmethod
    def retrieve_status(session: Session, status_id: int) -> Type[StatusModel]:
        db_status = (session.query(StatusModel).filter(StatusModel.id == status_id).first())

        if not db_status:
            raise StatusDoesNotExist()

        return db_status

    @classmethod
    def create_status(cls,
                      session: Session,
                      create_data: StatusUpsert) -> StatusModel:
        try:
            db_status = StatusModel(**create_data.model_dump())
            session.add(db_status)
            session.commit()
            return db_status

        except Exception as e:
            exc = CreateStatusException()
            logger.error(f"{exc.detail}. Details: {e}")
            raise exc

    @classmethod
    def partial_update_status(cls,
                              session: Session,
                              status_id: int,
                              update_data: StatusUpsert) -> Type[StatusModel]:
        db_status = cls.retrieve_status(session, status_id)
        update_data = update_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_status, key, value)

        try:
            session.commit()

        except Exception as e:
            exc = UpdateStatusException()
            logger.error(f"Error in StatusRepository::partial_update_status. "
                         f"{exc.detail}. Details: {e}")
            raise exc

        return db_status

    @classmethod
    def delete_status(cls, session: Session, status_id: int) -> bool:
        db_status = cls.retrieve_status(session, status_id)

        if not db_status:
            raise StatusDoesNotExist()

        try:
            session.delete(db_status)
            session.commit()
            return True

        except Exception as e:
            exc = DeleteStatusException()
            logger.error(f"Error in StatusRepository::delete_status. "
                         f"{exc.detail}. Details: {e}")
            raise exc
