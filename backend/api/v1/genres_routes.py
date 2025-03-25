from fastapi import (
    APIRouter,
    Depends,
    Request,
    Body,
)
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session

from utils.db_utils import get_db_session
from exceptions.genre_exceptions import DeleteGenreException
from repositories.genre_repository import GenreRepository
from services import authenticate
from permissions import IsAdmin

from schemas.genre_schema import (
    GenrePreview,
    GenreCreate,
    GenreUpdate,
)


router = APIRouter()


@router.get("/genres/", response_model=list[GenrePreview])
async def list_genres(session: Session = Depends(get_db_session)):
    return GenreRepository.list_genres(session)


@router.get("/genres/{genre_id}/", response_model=GenrePreview, status_code=200)
async def retrieve_genre(genre_id: int,
                         session: Session = Depends(get_db_session)):
    return GenreRepository.retrieve_genre(session, genre_id)


@router.post("/genres/", response_model=GenrePreview, status_code=201)
@authenticate
async def create_genre(request: Request,
                       create_data: GenreCreate,
                       session: Session = Depends(get_db_session)):
    IsAdmin.check_permissions(request)
    return GenreRepository.create_genre(session, create_data)


@router.patch("/genres/{genre_id}/", response_model=GenrePreview, status_code=200)
@authenticate
async def partial_update_genre(request: Request,
                               genre_id: int,
                               partial_update_data: GenreUpdate = Body(...),
                               session: Session = Depends(get_db_session)):
    IsAdmin.check_permissions(request)
    return GenreRepository.partial_update_genre(
        session, genre_id, partial_update_data
    )


@router.delete("/genres/{genre_id}/", status_code=200)
@authenticate
async def delete_genre(request: Request,
                       genre_id: int,
                       session: Session = Depends(get_db_session)):
    IsAdmin.check_permissions(request)

    is_deleted = GenreRepository.delete_genre(session, genre_id)

    if is_deleted:
        return JSONResponse(content={"details": "Genre deleted successfully."}, status_code=200)

    raise DeleteGenreException()
