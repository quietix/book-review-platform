from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import config, logger


def get_connection_url(db_name: str | None = None):
    return (f"postgresql://"
            f"{config.DB_USER}:"
            f"{config.DB_USER_PASSWORD}@"
            f"{config.DB_HOST}:"
            f"{config.DB_PORT}/"
            f"{db_name or config.DB_NAME}")


def get_connection_url_by_dbname(test_db: str):
    return (f"postgresql://"
            f"{config.DB_USER}:"
            f"{config.DB_USER_PASSWORD}@"
            f"{config.DB_HOST}:"
            f"{config.DB_PORT}/"
            f"{test_db}")


def _get_db_engine():
    postgres_url = get_connection_url()

    try:
        return create_engine(postgres_url, echo=config.DEBUG)
    except Exception as e:
        logger.error(f"Failed to get db engine. Details: {e}")
        raise e


def get_db_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


_engine = _get_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
