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
from exceptions.author_exceptions import DeleteAuthorException
from repositories.rating_repository import RatingRepository

from services import authenticate
from services.rating_service import RatingService

from permissions import UserIsOwner
from models import User as UserModel

from schemas.rating_schema import (
    RatingPreview,
    RatingDetails,
    RatingCreate,
    RatingUpdate,
)


router = APIRouter()


@router.get("/ratings/", response_model=list[RatingDetails])
async def list_ratings(session: Session = Depends(get_db_session)):
    return await RatingService.list_ratings(session)


@router.get("/ratings/{rating_id}/", response_model=RatingDetails, status_code=200)
async def retrieve_rating(rating_id: int,
                          session: Session = Depends(get_db_session)):
    return await RatingService.retrieve_rating(session, rating_id)


@router.post("/ratings/", response_model=RatingPreview, status_code=201)
@authenticate
async def create_rating(request: Request,
                        create_data: RatingCreate,
                        session: Session = Depends(get_db_session)):
    authed_user: UserModel = request.state.user
    return await asyncio.to_thread(
        RatingRepository.create_rating, session, create_data, authed_user
    )


@router.patch("/ratings/{rating_id}/", response_model=RatingPreview, status_code=200)
@authenticate
async def partial_update_rating(request: Request,
                                rating_id: int,
                                partial_update_data: RatingUpdate = Body(...),
                                session: Session = Depends(get_db_session)):
    db_rating = await asyncio.to_thread(RatingRepository.retrieve_rating, session, rating_id)
    UserIsOwner.check_permissions(request, db_rating)
    return await asyncio.to_thread(
        RatingRepository.partial_update_rating, session, rating_id, partial_update_data
    )


@router.delete("/ratings/{rating_id}/", status_code=200)
@authenticate
async def delete_rating(request: Request,
                        rating_id: int,
                        session: Session = Depends(get_db_session)):
    db_rating = RatingRepository.retrieve_rating(session, rating_id)
    UserIsOwner.check_permissions(request, db_rating)

    is_deleted = await asyncio.to_thread(
        RatingRepository.delete_rating, session, rating_id
    )

    if is_deleted:
        return JSONResponse(content={"details": "Rating deleted successfully."}, status_code=200)

    raise DeleteAuthorException()
