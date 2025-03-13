from sqlmodel import Session, SQLModel, create_engine

from config import config, logger


def get_connection_url():
    return (f"postgresql://"
            f"{config.DB_USER}:"
            f"{config.DB_USER_PASSWORD}@"
            f"{config.DB_HOST}:"
            f"{config.DB_PORT}/"
            f"{config.DB_NAME}")


def _get_db_engine():
    postgres_url = get_connection_url()

    try:
        engine = create_engine(postgres_url, echo=config.DEBUG)
        return engine
    except Exception as e:
        logger.error(f"Failed to get db engine. Details: {e}")
        raise e


def init_db():
    SQLModel.metadata.create_all(_engine)


def get_db_session() -> Session:
    with Session(_engine) as session:
        yield session


_engine = _get_db_engine()
