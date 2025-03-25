from typing import Optional

from pydantic import BaseModel, ConfigDict


class BaseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: str
    name: Optional[str] = None
    surname: Optional[str] = None


class UserPreview(BaseUser):
    id: int


class UserNestedPreview(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    name: Optional[str]
    surname: Optional[str]


class UserDetails(UserPreview):
    is_admin: bool
    hashed_password: bytes


class UserUpsert(BaseUser):
    password: str


class UserPartialUpdate(UserUpsert):
    username: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    password: Optional[str] = None
