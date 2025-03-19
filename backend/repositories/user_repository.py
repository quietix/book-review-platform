from typing import Type

from sqlalchemy.orm import Session

from utils.security_utils import get_hashed_password
from config import logger
from models import User as UserModel

from schemas import (
    UserUpsert,
    UserPartialUpdate
)

from excepitons import (
    UserDoesNotExist,
    CreateUserException,
    UpdateUserException,
    DeleteUserException
)


class UserRepository:
    @staticmethod
    def list_users(session: Session) -> list[Type[UserModel]]:
        return session.query(UserModel).all()

    @staticmethod
    def retrieve_user(session: Session, user_id: int) -> UserModel:
        db_user = session.get(UserModel, user_id)

        if not db_user:
            raise UserDoesNotExist()

        return db_user

    @staticmethod
    def retrieve_user_by_username(session: Session, username: str) -> UserModel:
        db_user = session.query(UserModel).filter(UserModel.username == username).first()

        if not db_user:
            raise UserDoesNotExist()

        return db_user

    @staticmethod
    def create_user(session: Session, user: UserUpsert) -> UserModel:
        hashed_password = get_hashed_password(user.password)

        if 'username' in user.model_dump(exclude_unset=True):
            new_username = user.username
            if session.query(UserModel).filter(UserModel.username == new_username).first():
                raise CreateUserException(detail="Username is already taken.")

        if 'email' in user.model_dump(exclude_unset=True):
            new_email = user.email
            if session.query(UserModel).filter(UserModel.email == new_email).first():
                raise CreateUserException(detail="Email is already taken.")

        try:
            db_user = UserModel(
                **user.model_dump(exclude={"password"}),
                hashed_password=hashed_password
            )

            session.add(db_user)
            session.commit()

        except Exception as e:
            logger.error(f"Failed to create user. Details: {e}")
            raise CreateUserException()

        return db_user

    @classmethod
    def update_user(cls,
                    session: Session,
                    user_id: int,
                    user: UserUpsert) -> UserModel:
        db_user: UserModel = cls.retrieve_user(session, user_id)

        if 'username' in user.model_dump(exclude_unset=True):
            new_username = user.username
            if session.query(UserModel).filter(
                    UserModel.username == new_username,
                    UserModel.id != user_id
            ).first():
                raise UpdateUserException(detail="Username is already taken.")

        if 'email' in user.model_dump(exclude_unset=True):
            new_email = user.email
            if session.query(UserModel).filter(
                    UserModel.email == new_email,
                    UserModel.id != user_id
            ).first():
                raise UpdateUserException(detail="Email is already taken.")

        update_data = user.model_dump(exclude_unset=False)

        if not all(update_data.values()):
            raise UpdateUserException(detail="All fields must be provided.")

        for key, value in update_data.items():
            if key == 'password':
                setattr(db_user, 'hashed_password', get_hashed_password(value))
            else:
                setattr(db_user, key, value)

        try:
            session.commit()
        except Exception as e:
            logger.error(f"Failed to update user. Details: {e}")
            raise UpdateUserException()

        return db_user

    @classmethod
    def partial_update_user(cls,
                            session: Session,
                            user_id: int,
                            user: UserPartialUpdate) -> UserModel:
        db_user: UserModel = cls.retrieve_user(session, user_id)

        if 'username' in user.model_dump(exclude_unset=True):
            new_username = user.username
            if session.query(UserModel).filter(
                    UserModel.username == new_username,
                    UserModel.id != user_id
            ).first():
                raise UpdateUserException(detail="Username is already taken.")

        if 'email' in user.model_dump(exclude_unset=True):
            new_email = user.email
            if session.query(UserModel).filter(
                    UserModel.email == new_email,
                    UserModel.id != user_id
            ).first():
                raise UpdateUserException(detail="Email is already taken.")

        update_data = user.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if key == 'password':
                setattr(db_user, 'hashed_password', get_hashed_password(value))
            else:
                setattr(db_user, key, value)

        try:
            session.commit()

        except Exception as e:
            logger.error(f"Failed to update user. Details: {e}")
            raise UpdateUserException()

        return db_user

    @classmethod
    def delete_user(cls, session: Session, user_id: int) -> bool:
        db_user = cls.retrieve_user(session, user_id)

        if not db_user:
            raise UserDoesNotExist()

        try:
            session.delete(db_user)
            session.commit()
            return True

        except Exception as e:
            logger.error(f"Failed to delete user. Details: {e}")
            raise DeleteUserException(detail="Failed to delete user.")
