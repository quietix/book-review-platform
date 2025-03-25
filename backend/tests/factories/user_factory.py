import factory

from faker import Faker

from models import User as UserModel
from utils.security_utils import get_hashed_password
from schemas import UserUpsert


fake = Faker()


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserModel
        sqlalchemy_session_persistence = "commit"

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    password = factory.Faker("password")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        if "password" in kwargs:
            kwargs["hashed_password"] = get_hashed_password(kwargs.pop("password"))
        return super()._create(model_class, *args, **kwargs)


class UserUpsertDataFactory(factory.Factory):
    class Meta:
        model = UserUpsert

    username = factory.LazyAttribute(lambda _: fake.user_name())
    email = factory.LazyAttribute(lambda _: fake.email())
    name = factory.LazyAttribute(lambda _: fake.first_name())
    surname = factory.LazyAttribute(lambda _: fake.last_name())
    password = factory.LazyAttribute(lambda _: fake.password())
