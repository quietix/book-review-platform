# from threading import Lock
#
# from sqlalchemy import Sequence
# from sqlmodel import Session, select
#
# from .models import User
#
#
# class SingletonMeta(type):
#     _instances = {}
#     _lock: Lock = Lock()
#
#     def __call__(cls, *args, **kwargs):
#         with cls._lock:
#             if cls not in cls._instances:
#                 instance = super().__call__(*args, **kwargs)
#                 cls._instances[cls] = instance
#         return cls._instances[cls]
#
#
# class UserRepository(metaclass=SingletonMeta):
#     def __init__(self, session: Session):
#         self.session = session
#
#     def get_users(self) -> Sequence[User]:
#         statement = select(User)
#         results = self.session.exec(statement)
#         return results.all()
