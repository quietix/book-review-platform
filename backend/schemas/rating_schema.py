from typing import Optional

from pydantic import BaseModel, ConfigDict

from .user_schema import UserPreview
from .book_schema import BookDetails


class BaseRating(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RatingPreview(BaseRating):
    id: int
    book_id: int
    user_id: int
    rating: int


class PratingNestedPreview(BaseRating):
    id: int
    rating: int


class RatingDetails(BaseRating):
    id: int
    book: BookDetails
    user: UserPreview
    rating: int


class RatingCreate(BaseRating):
    book_id: int
    rating: int


class RatingUpdate(BaseRating):
    book_id: Optional[int] = None
    rating: Optional[int] = None
