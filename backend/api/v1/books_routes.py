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
from repositories.book_repository import BookRepository

from services.book_service import BookService
from services import authenticate

from permissions import UserIsPublisher
from models import User as UserModel

from schemas.book_schema import (
    BookPreview,
    BookDetails,
    BookCreateManually,
    BookCreateByIsbn,
    BookPartialUpdate,
    BookRecommendations,
)


router = APIRouter()


@router.get("/books/", response_model=list[BookDetails])
async def list_books(session: Session = Depends(get_db_session)):
    return await BookService.list_books(session)


@router.get("/books/{book_id}/", response_model=BookDetails, status_code=200)
async def retrieve_book(book_id: int,
                        session: Session = Depends(get_db_session)):
    return await BookService.retrieve_book(session, book_id)


@router.get("/recommendations/", response_model=list[BookRecommendations])
@authenticate
async def list_recommendations(request: Request,
                               session: Session = Depends(get_db_session)):
    authed_user: UserModel = request.state.user
    res = await asyncio.to_thread(BookRepository.get_recommendations, session, authed_user)
    return res


@router.post("/books/create-manually/", response_model=BookPreview, status_code=201)
@authenticate
async def create_book_manually(request: Request,
                               create_data: BookCreateManually,
                               session: Session = Depends(get_db_session)):
    authed_user: UserModel = request.state.user
    return await asyncio.to_thread(
        BookRepository.create_book_manually, session, create_data, authed_user
    )


@router.post("/books/create-by-isbn/", response_model=BookPreview, status_code=201)
@authenticate
async def create_book_by_isbn(request: Request,
                              create_data: BookCreateByIsbn,
                              session: Session = Depends(get_db_session)):
    authed_user: UserModel = request.state.user
    return await BookService.create_book_by_isbn(session, authed_user, create_data)


@router.patch("/books/{book_id}/", response_model=BookPreview, status_code=200)
@authenticate
async def partial_update_book(request: Request,
                              book_id: int,
                              partial_update_data: BookPartialUpdate = Body(...),
                              session: Session = Depends(get_db_session)):
    db_author = BookRepository.retrieve_book(session, book_id)
    UserIsPublisher.check_permissions(request, db_author)
    return await asyncio.to_thread(
        BookRepository.partial_update_book, session, book_id, partial_update_data
    )


@router.delete("/books/{book_id}/", status_code=200)
@authenticate
async def delete_book(request: Request,
                      book_id: int,
                      session: Session = Depends(get_db_session)):
    db_author = BookRepository.retrieve_book(session, book_id)
    UserIsPublisher.check_permissions(request, db_author)

    is_deleted = await asyncio.to_thread(
        BookRepository.delete_book, session, book_id
    )

    if is_deleted:
        return JSONResponse(content={"details": "Book deleted successfully."}, status_code=200)

    raise DeleteAuthorException()
