from sqlalchemy.orm import declarative_base


Base = declarative_base()

from .user_model import User # NOQA

__all__ = ['User']
