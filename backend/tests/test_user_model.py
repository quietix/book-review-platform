from sqlalchemy.orm import Session

from models import User as UserModel
from tests.factories import UserFactory


class TestUserDatabase:

    def test_create_user(self, db: Session):
        user = UserFactory()

        db.add(user)
        db.commit()
        db.refresh(user)

        assert user.id is not None
        assert user.username is not None
        assert user.email is not None

    def test_create_multiple_users(self, db: Session):
        users = UserFactory.create_batch(5)

        assert len(users) == 5

        for user in users:
            assert user.id is not None
            assert user.username is not None
            assert user.email is not None

    def test_read_user(self, db: Session):
        user_data = UserFactory.create()
        db_user = db.get(UserModel, user_data.id)

        assert db_user
        assert db_user.id == user_data.id
        assert db_user.username == user_data.username
        assert db_user.email == user_data.email
        assert db_user.name == user_data.name
        assert db_user.surname == user_data.surname
        assert db_user.hashed_password == user_data.hashed_password

    def test_update_user(self, db: Session):
        user_data = UserFactory.create()

        db_user = db.get(UserModel, user_data.id)
        assert db_user.id != "UpdatedUsername"

        user_data.username = "UpdatedUsername"
        db.commit()
        db.refresh(user_data)

        db_user = db.get(UserModel, user_data.id)
        assert db_user.username == "UpdatedUsername"

    def test_delete_user(self, db: Session):
        user_data = UserFactory.create()

        db_user = db.get(UserModel, user_data.id)
        assert db_user

        db.delete(user_data)
        db.commit()

        deleted_user = db.get(UserModel, user_data.id)
        assert deleted_user is None
