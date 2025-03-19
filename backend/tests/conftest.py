import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session

from utils.db_utils import get_db_session
from utils.auth_utils import create_access_token

from models import Base
from tests.factories import UserFactory
from main import app


TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    engine = create_engine(
        url=TEST_DATABASE_URL,
        connect_args={
            "check_same_thread": False,
        },
        poolclass=StaticPool
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    yield engine, TestingSessionLocal

    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db(setup_test_database):
    engine, TestingSession = setup_test_database

    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSession(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(autouse=True)
def set_session_for_factories(db: Session):
    UserFactory._meta.sqlalchemy_session = db


@pytest.fixture
def client(db: Session):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db_session] = override_get_db
    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def authenticated_client(db: Session):
    user = UserFactory.create()
    token = create_access_token({"sub": user.username})

    def override_get_db():
        yield db

    app.dependency_overrides[get_db_session] = override_get_db
    with TestClient(app) as c:
        c.headers["Authorization"] = f"Bearer {token}"
        yield c, user

    app.dependency_overrides.clear()
