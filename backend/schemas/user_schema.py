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


class UserDetails(UserPreview):
    hashed_password: bytes


class UserCreate(BaseUser):
    password: str


class UserUpdate(UserPreview):
    password: str
