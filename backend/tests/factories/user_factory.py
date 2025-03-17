import factory
from models import User
from utils import get_hashed_password


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
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
