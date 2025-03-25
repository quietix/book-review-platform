import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from schemas.book_schema import BookNestedPreview
from schemas.status_schema import StatusPreview


class BaseReadingItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ReadingItemPreview(BaseReadingItem):
    id: int
    user_id: int
    book_id: int
    status_id: int
    published_at: datetime.datetime
    updated_at: datetime.datetime


class ReadingItemDetails(BaseReadingItem):
    id: int
    book: BookNestedPreview
    status: StatusPreview
    published_at: datetime.datetime
    updated_at: datetime.datetime


class ReadingItemCreate(BaseReadingItem):
    book_id: int
    status_id: int


class ReadingItemUpdate(BaseReadingItem):
    status_id: Optional[int] = None
