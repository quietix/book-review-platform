from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .user_schema import UserPreview


class BaseAuthor(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AuthorDetails(BaseAuthor):
    id: int
    name: str
    surname: str
    published_at: datetime
    updated_at: datetime
    publisher: Optional[UserPreview]


class AuthorPreview(BaseAuthor):
    id: int
    name: str
    surname: str
    published_at: datetime
    updated_at: datetime
    publisher_id: Optional[int]


class AuthorCreate(BaseAuthor):
    name: str
    surname: str


class AuthorPartialUpdate(BaseAuthor):
    name: Optional[str] = None
    surname: Optional[str] = None
