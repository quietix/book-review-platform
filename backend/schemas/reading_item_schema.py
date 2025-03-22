from pydantic import BaseModel, ConfigDict

from schemas.user_schema import UserNestedPreview
from schemas.book_schema import BookNestedPreview
from schemas.status_schema import StatusPreview


class BaseReadingItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ReadingItemPreview(BaseReadingItem):
    id: int
    user_id: int
    book_id: int
    status_id: int


class ReadingItemDetails(BaseReadingItem):
    id: int
    user: UserNestedPreview
    book: BookNestedPreview
    status: StatusPreview


class ReadingItemCreate(BaseReadingItem):
    book_id: int
    status_id: int
