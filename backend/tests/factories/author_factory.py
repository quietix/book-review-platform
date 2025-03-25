import factory

from faker import Faker

from .user_factory import UserFactory
from models import Author as AuthorModel
from schemas.author_schema import AuthorCreate


fake = Faker()


class AuthorFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = AuthorModel
        sqlalchemy_session_persistence = "commit"

    publisher = factory.SubFactory(UserFactory)
    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")


class AuthorCreateDataFactory(factory.Factory):
    class Meta:
        model = AuthorCreate

    name = factory.LazyAttribute(lambda _: fake.first_name())
    surname = factory.LazyAttribute(lambda _: fake.last_name())
