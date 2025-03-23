from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .user_schema import UserPreview
from .author_schema import AuthorPreview, AuthorNestedPreview
from .genre_schema import GenrePreview


class BaseBook(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BookPreview(BaseBook):
    id: int
    author_id: int
    publisher_id: Optional[int]
    genre_id: Optional[int]
    isbn: Optional[str]
    title: str
    description: Optional[str]
    published_at: datetime
    updated_at: datetime


class BookNestedPreview(BaseBook):
    id: int
    genre: Optional[GenrePreview]
    isbn: Optional[str]
    title: str


class BookDetails(BaseBook):
    id: int
    author: AuthorPreview
    publisher: Optional[UserPreview]
    genre: Optional[GenrePreview]
    isbn: Optional[str]
    title: str
    description: Optional[str]
    published_at: datetime
    updated_at: datetime


class BookRecommendations(BaseBook):
    id: int
    author: AuthorNestedPreview
    publisher: Optional[UserPreview]
    genre: Optional[GenrePreview]
    title: str


class BookCreateManually(BaseBook):
    author_id: int
    genre_id: Optional[int] = None
    isbn: Optional[str] = None
    title: str
    description: Optional[str] = None


class BookCreateByIsbn(BaseBook):
    isbn: str


class BookAutomaticCreationByIsbn(BaseBook):
    author_id: Optional[int] = None
    publisher_id: Optional[int] = None
    isbn: Optional[str] = None
    title: str
    description: str


class BookPartialUpdate(BaseBook):
    author_id: Optional[int] = None
    publisher_id: Optional[int] = None
    genre_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
