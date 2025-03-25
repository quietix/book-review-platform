from fastapi import (
    APIRouter,
    Depends,
    Request,
    Body,
)
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session

from utils.db_utils import get_db_session
from exceptions.status_exceptions import DeleteStatusException
from repositories.status_repository import StatusRepository
from services import authenticate
from permissions import IsAdmin

from schemas.status_schema import (
    StatusPreview,
    StatusUpsert,
)


router = APIRouter()


@router.get("/statuses/", response_model=list[StatusPreview])
async def list_statuses(session: Session = Depends(get_db_session)):
    return StatusRepository.list_statuses(session)


@router.get("/statuses/{status_id}/", response_model=StatusPreview, status_code=200)
async def retrieve_status(status_id: int,
                          session: Session = Depends(get_db_session)):
    return StatusRepository.retrieve_status(session, status_id)


@router.post("/statuses/", response_model=StatusPreview, status_code=201)
@authenticate
async def create_status(request: Request,
                        create_data: StatusUpsert,
                        session: Session = Depends(get_db_session)):
    IsAdmin.check_permissions(request)
    return StatusRepository.create_status(session, create_data)


@router.patch("/statuses/{status_id}/", response_model=StatusPreview, status_code=200)
@authenticate
async def partial_update_status(request: Request,
                                status_id: int,
                                partial_update_data: StatusUpsert = Body(...),
                                session: Session = Depends(get_db_session)):
    IsAdmin.check_permissions(request)
    return StatusRepository.partial_update_status(
        session, status_id, partial_update_data
    )


@router.delete("/statuses/{status_id}/", status_code=200)
@authenticate
async def delete_status(request: Request,
                        status_id: int,
                        session: Session = Depends(get_db_session)):
    IsAdmin.check_permissions(request)

    is_deleted = StatusRepository.delete_status(session, status_id)

    if is_deleted:
        return JSONResponse(content={"details": "Status deleted successfully."}, status_code=200)

    raise DeleteStatusException()
