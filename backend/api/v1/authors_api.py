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
from repositories.author_repository import AuthorRepository
from services.author_service import AuthorService
from services import authenticate
from permissions import UserIsPublisher
from models import User as UserModel

from schemas.author_schema import (
    AuthorPreview,
    AuthorDetails,
    AuthorCreate,
    AuthorPartialUpdate,
)


router = APIRouter()


@router.get("/authors/", response_model=list[AuthorDetails])
async def list_authors(session: Session = Depends(get_db_session)):
    return AuthorService.list_authors(session)


@router.get("/authors/{author_id}/", response_model=AuthorDetails, status_code=200)
async def retrieve_author(author_id: int,
                          session: Session = Depends(get_db_session)):
    return AuthorService.retrieve_author(session, author_id)


@router.post("/authors/", response_model=AuthorPreview, status_code=201)
@authenticate
async def create_author(request: Request,
                        create_data: AuthorCreate,
                        session: Session = Depends(get_db_session)):
    authed_user: UserModel = request.state.user
    return AuthorRepository.create_author(session, create_data, authed_user)


@router.patch("/authors/{author_id}/", response_model=AuthorPreview, status_code=200)
@authenticate
async def partial_update_author(request: Request,
                                author_id: int,
                                partial_update_data: AuthorPartialUpdate = Body(...),
                                session: Session = Depends(get_db_session)):
    db_author = AuthorRepository.retrieve_author(session, author_id)
    UserIsPublisher.check_permissions(request, db_author)
    return AuthorRepository.partial_update_author(session,
                                                  author_id,
                                                  partial_update_data)


@router.delete("/authors/{author_id}/", status_code=200)
@authenticate
async def delete_author(request: Request,
                        author_id: int,
                        session: Session = Depends(get_db_session)):
    db_author = AuthorRepository.retrieve_author(session, author_id)
    UserIsPublisher.check_permissions(request, db_author)

    is_deleted = AuthorRepository.delete_author(session, author_id)

    if is_deleted:
        return JSONResponse(content={"details": "User deleted successfully."}, status_code=200)

    raise DeleteAuthorException()
