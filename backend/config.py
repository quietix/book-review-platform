import logging
import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    def __init__(self):
        self._setup_app()
        self._setup_db()


    def _setup_app(self):
        self.DEBUG = bool(os.getenv("DEBUG"))

    def _setup_db(self):
        self.DB_NAME = os.getenv("DB_NAME")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_USER_PASSWORD = os.getenv("DB_USER_PASSWORD")
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = os.getenv("DB_PORT")

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
