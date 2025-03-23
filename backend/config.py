import logging
import os

from dotenv import load_dotenv

from excepitons import ConfigurationError


load_dotenv()


class Config:
    def __init__(self):
        self._setup_app()
        self._setup_admin_user()
        self._setup_db()
        self._setup_isbndb()
        self.validate_variables()

    def validate_variables(self):
        if not all(vars(self)):
            raise ConfigurationError()

    def _setup_app(self):
        self.DEBUG = bool(os.getenv("DEBUG"))

        ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS")
        if ALLOWED_ORIGINS:
            self.ALLOWED_ORIGINS = ALLOWED_ORIGINS.split(',')

        self.AUTH_ALGORITHM = os.getenv("AUTH_ALGORITHM")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
        self.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

        self.FINISHED_BOOKS_STATUS_NAME = os.getenv("FINISHED_BOOKS_STATUS_NAME")

    def _setup_admin_user(self):
        self.ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
        self.ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
        self.ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    def _setup_db(self):
        self.DB_NAME = os.getenv("DB_NAME")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_USER_PASSWORD = os.getenv("DB_USER_PASSWORD")
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = os.getenv("DB_PORT")

    def _setup_isbndb(self):
        self.ISBNDB_API_KEY = os.getenv("ISBNDB_API_KEY")
        self.ISBNDB_API_URL = os.getenv("ISBNDB_API_URL")

    def __str__(self):
        return str([f"{key}: {value}" for key, value in vars(self).items()])


def setup_logger():
    logger = logging.getLogger("fastapi_project")

    logger.setLevel(logging.DEBUG) if config.DEBUG else logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


config = Config()

logger = setup_logger()
