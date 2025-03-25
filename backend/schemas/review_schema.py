import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from .user_schema import UserNestedPreview
from .book_schema import BookNestedPreview
from .rating_schema import PratingNestedPreview


class BaseReview(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ReviewPreview(BaseReview):
    id: int
    publisher_id: int
    book_id: int
    rating_id: Optional[int]
    title: str
    text: Optional[str]
    published_at: datetime.datetime
    updated_at: datetime.datetime


class ReviewDetails(BaseReview):
    id: int
    title: str
    text: Optional[str]
    published_at: datetime.datetime
    updated_at: datetime.datetime
    rating: Optional[PratingNestedPreview]
    publisher: UserNestedPreview
    book: BookNestedPreview


class ReviewCreate(BaseReview):
    book_id: int
    rating: Optional[int] = None
    title: str
    text: Optional[str] = None


class ReviewUpdate(BaseReview):
    title: Optional[str] = None
    text: Optional[str] = None
