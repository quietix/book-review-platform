import pytest
from sqlalchemy.orm import Session

from models import User as UserModel
from tests.factories import UserFactory, UserUpsertDataFactory
from repositories import UserRepository
from schemas import UserPartialUpdate
from exceptions.user_exceptions import (
    UserDoesNotExist,
    CreateUserException,
    UpdateUserException
)


class TestUserRead:
    def test_read_user(self, db: Session):
        created_user = UserFactory.create()

        db_user = UserRepository.retrieve_user(db, created_user.id)

        assert db_user
        assert db_user.id == created_user.id
        assert db_user.username == created_user.username
        assert db_user.email == created_user.email
        assert db_user.name == created_user.name
        assert db_user.surname == created_user.surname
        assert db_user.hashed_password == created_user.hashed_password


class TestUserCreate:
    def test_create_user(self, db: Session):
        upsert_user_data = UserUpsertDataFactory()
        created_user = UserRepository.create_user(db, upsert_user_data)

        db_user = db.get(UserModel, created_user.id)

        assert db_user.id == created_user.id
        assert db_user.username == created_user.username
        assert db_user.email == created_user.email
        assert db_user.name == created_user.name
        assert db_user.surname == created_user.surname
        assert db_user.hashed_password == created_user.hashed_password

    def test_create_multiple_users(self, db: Session):
        users = UserUpsertDataFactory.create_batch(5)

        for user in users:
            UserRepository.create_user(db, user)

        db_users = db.query(UserModel).all()

        assert len(db_users) == 5

        for user, db_user in zip(users, db_users):
            assert user.username == db_user.username
            assert user.email == db_user.email
            assert user.name == db_user.name
            assert user.surname == db_user.surname
            assert db_user.hashed_password != user.password

    def test_create_user_with_existing_username(self, db: Session):
        user_data_1 = UserUpsertDataFactory.create(username="duplicate_username")
        user_data_2 = UserUpsertDataFactory.create(username="duplicate_username")

        UserRepository.create_user(db, user_data_1)

        with pytest.raises(CreateUserException):
            UserRepository.create_user(db, user_data_2)

    def test_create_user_with_existing_email(self, db: Session):
        user_data_1 = UserUpsertDataFactory.create(email="duplicate@example.com")
        user_data_2 = UserUpsertDataFactory.create(email="duplicate@example.com")

        UserRepository.create_user(db, user_data_1)

        with pytest.raises(CreateUserException):
            UserRepository.create_user(db, user_data_2)


class TestUserUpdate:
    def test_update_user(self, db: Session):
        create_data = UserUpsertDataFactory.create()
        created_user = UserRepository.create_user(db, create_data)

        update_data = UserUpsertDataFactory.create()
        updated_user = UserRepository.update_user(db, created_user.id, update_data)

        db_user = UserRepository.retrieve_user(db, created_user.id)

        assert db_user.id == updated_user.id
        assert db_user.username == updated_user.username
        assert db_user.email == updated_user.email
        assert db_user.name == updated_user.name
        assert db_user.surname == updated_user.surname
        assert db_user.hashed_password == updated_user.hashed_password

    def test_partial_update_user(self, db: Session):
        create_data = UserUpsertDataFactory.create()
        created_user = UserRepository.create_user(db, create_data)

        update_data = UserPartialUpdate(username="updated_username")
        updated_user = UserRepository.partial_update_user(db, created_user.id, update_data)

        db_user = UserRepository.retrieve_user(db, created_user.id)

        assert db_user.id == updated_user.id
        assert db_user.username == updated_user.username
        assert db_user.email == updated_user.email
        assert db_user.name == updated_user.name
        assert db_user.surname == updated_user.surname
        assert db_user.hashed_password == updated_user.hashed_password

    def test_update_user_change_username_to_existing(self, db: Session):
        user_data_1 = UserUpsertDataFactory(username="existing_username")
        user_data_2 = UserUpsertDataFactory(username="duplicate_username")

        created_user_1 = UserRepository.create_user(db, user_data_1)
        UserRepository.create_user(db, user_data_2)

        with pytest.raises(UpdateUserException):
            UserRepository.update_user(db, created_user_1.id, user_data_2)

    def test_update_user_change_email_to_existing(self, db: Session):
        user_data_1 = UserUpsertDataFactory(email="existing_email@example.com")
        user_data_2 = UserUpsertDataFactory(email="duplicate_email@example.com")

        created_user_1 = UserRepository.create_user(db, user_data_1)
        UserRepository.create_user(db, user_data_2)

        with pytest.raises(UpdateUserException):
            UserRepository.update_user(db, created_user_1.id, user_data_2)

    def test_partial_update_user_change_username_to_existing(self, db: Session):
        user_data_1 = UserUpsertDataFactory(username="existing_username")
        user_data_2 = UserUpsertDataFactory(username="duplicate_username")

        created_user_1 = UserRepository.create_user(db, user_data_1)
        UserRepository.create_user(db, user_data_2)

        partial_update_data = UserPartialUpdate(username="duplicate_username")

        with pytest.raises(UpdateUserException):
            UserRepository.partial_update_user(db, created_user_1.id, partial_update_data)

    def test_partial_user_change_email_to_existing(self, db: Session):
        user_data_1 = UserUpsertDataFactory(email="existing_email@example.com")
        user_data_2 = UserUpsertDataFactory(email="duplicate_email@example.com")

        created_user_1 = UserRepository.create_user(db, user_data_1)
        UserRepository.create_user(db, user_data_2)

        partial_update_data = UserPartialUpdate(email="duplicate_email@example.com")

        with pytest.raises(UpdateUserException):
            UserRepository.partial_update_user(db, created_user_1.id, partial_update_data)


class TestUserDelete:
    def test_delete_user(self, db: Session):
        created_user = UserFactory.create()

        db_user = UserRepository.retrieve_user(db, created_user.id)
        assert db_user

        UserRepository.delete_user(db, created_user.id)

        with pytest.raises(UserDoesNotExist):
            UserRepository.retrieve_user(db, created_user.id)
