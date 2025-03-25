import asyncio
from typing import List

from sqlalchemy.orm import Session

from models import User as UserModel
from schemas.reading_item_schema import ReadingItemDetails
from repositories.reading_item_repository import ReadingItemRepository


class ReadingItemService:
    @classmethod
    async def list_reading_items(cls,
                                 session: Session,
                                 authed_user: UserModel) -> List[ReadingItemDetails]:
        reading_items = await asyncio.to_thread(
            ReadingItemRepository.list_reading_items_and_prefetch, session, authed_user
        )
        return [ReadingItemDetails.model_validate(reading_item) for reading_item in reading_items]

    @classmethod
    async def retrieve_reading_item(cls,
                                    session: Session,
                                    reading_item_id: int,
                                    authed_user: UserModel) -> ReadingItemDetails:
        db_reading_item = await asyncio.to_thread(
            ReadingItemRepository.retrieve_reading_item_and_prefetch,
            session,
            reading_item_id,
            authed_user
        )
        return ReadingItemDetails.model_validate(db_reading_item)
