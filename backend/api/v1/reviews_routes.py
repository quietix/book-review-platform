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
from excepitons.author_exceptions import DeleteAuthorException
from repositories.review_repository import ReviewRepository

from services import authenticate
from services.review_service import ReviewService

from permissions import UserIsPublisher
from models import User as UserModel

from schemas.review_schema import (
    ReviewPreview,
    ReviewDetails,
    ReviewCreate,
    ReviewUpdate,
)


router = APIRouter()


@router.get("/reviews/", response_model=list[ReviewDetails])
async def list_reviews(session: Session = Depends(get_db_session)):
    return await ReviewService.list_reviews(session)


@router.get("/reviews/{review_id}/", response_model=ReviewDetails, status_code=200)
async def retrieve_review(review_id: int,
                          session: Session = Depends(get_db_session)):
    return await ReviewService.retrieve_review(session, review_id)


@router.post("/reviews/", response_model=ReviewPreview, status_code=201)
@authenticate
async def create_review(request: Request,
                        create_data: ReviewCreate,
                        session: Session = Depends(get_db_session)):
    authed_user: UserModel = request.state.user
    return await asyncio.to_thread(
        ReviewRepository.create_review, session, create_data, authed_user
    )


@router.patch("/reviews/{review_id}/", response_model=ReviewPreview, status_code=200)
@authenticate
async def partial_update_review(request: Request,
                                review_id: int,
                                partial_update_data: ReviewUpdate = Body(...),
                                session: Session = Depends(get_db_session)):
    db_review = await asyncio.to_thread(ReviewRepository.retrieve_review, session, review_id)
    UserIsPublisher.check_permissions(request, db_review)
    return await asyncio.to_thread(
        ReviewRepository.partial_update_review, session, review_id, partial_update_data
    )


@router.delete("/reviews/{review_id}/", status_code=200)
@authenticate
async def delete_review(request: Request,
                        review_id: int,
                        session: Session = Depends(get_db_session)):
    db_review = ReviewRepository.retrieve_review(session, review_id)
    UserIsPublisher.check_permissions(request, db_review)

    is_deleted = await asyncio.to_thread(
        ReviewRepository.delete_review, session, review_id
    )

    if is_deleted:
        return JSONResponse(content={"details": "Review deleted successfully."}, status_code=200)

    raise DeleteAuthorException()
