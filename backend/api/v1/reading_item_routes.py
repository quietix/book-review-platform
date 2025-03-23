import asyncio

from fastapi import (
    APIRouter,
    Depends,
    Request,
    Body,
)
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session

from utils.db_utils import get_db_session
from excepitons.status_exceptions import DeleteStatusException
from repositories.reading_item_repository import ReadingItemRepository

from services import authenticate
from services.reading_item_service import ReadingItemService

from models import User as UserModel

from schemas.reading_item_schema import (
    ReadingItemPreview,
    ReadingItemDetails,
    ReadingItemCreate,
    ReadingItemUpdate,
)


router = APIRouter()


@router.get("/my-reading-list/", response_model=list[ReadingItemDetails])
@authenticate
async def list_reading_items(request: Request,
                             session: Session = Depends(get_db_session)):
    authed_user: UserModel = request.state.user
    return await ReadingItemService.list_reading_items(session, authed_user)


@router.get("/my-reading-list/{reading_item_id}/",
            response_model=ReadingItemDetails,
            status_code=200)
@authenticate
async def retrieve_review(request: Request,
                          reading_item_id: int,
                          session: Session = Depends(get_db_session)):
    authed_user: UserModel = request.state.user
    return await ReadingItemService.retrieve_reading_item(session, reading_item_id, authed_user)


@router.post("/my-reading-list/", response_model=ReadingItemPreview, status_code=200)
@authenticate
async def create_reading_item(request: Request,
                              create_data: ReadingItemCreate,
                              session: Session = Depends(get_db_session)):
    authed_user: UserModel = request.state.user
    return await asyncio.to_thread(
        ReadingItemRepository.create_reading_item, session, create_data, authed_user
    )


@router.patch("/my-reading-list/{reading_item_id}/",
              response_model=ReadingItemPreview,
              status_code=200)
@authenticate
async def partial_update_reading_item(request: Request,
                                      reading_item_id: int,
                                      partial_update_data: ReadingItemUpdate = Body(...),
                                      session: Session = Depends(get_db_session)):
    authed_user: UserModel = request.state.user
    return await asyncio.to_thread(
        ReadingItemRepository.partial_update_reading_item,
        session,
        reading_item_id,
        partial_update_data,
        authed_user
    )


@router.delete("/my-reading-list/{reading_item_id}/", status_code=200)
@authenticate
async def delete_reading_item(request: Request,
                              reading_item_id: int,
                              session: Session = Depends(get_db_session)):
    authed_user: UserModel = request.state.user

    is_deleted = await asyncio.to_thread(
        ReadingItemRepository.delete_reading_item, session, reading_item_id, authed_user
    )

    if is_deleted:
        return JSONResponse(content={"details": "Status deleted successfully."}, status_code=200)

    raise DeleteStatusException()
