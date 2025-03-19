from fastapi import (
    APIRouter,
    Depends,
    Request,
)
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session

from utils.db_utils import get_db_session

from repositories import UserRepository
from excepitons import DeleteUserException
from services import authenticate
from permissions import IsProfileOwner
from models import User as UserModel

from schemas import (
    UserDetails,
    UserUpsert,
    UserPartialUpdate,
)


router = APIRouter()


@router.get("/profile/", response_model=UserDetails)
@authenticate
async def retrieve_profile(request: Request,
                           session: Session = Depends(get_db_session)):
    authed_user: UserModel = request.state.user
    IsProfileOwner.check_permissions(request, authed_user)
    return UserRepository.retrieve_user(session, authed_user.id)


@router.put("/profile/", response_model=UserDetails, status_code=200)
@authenticate
async def update_profile(request: Request,
                         update_data: UserUpsert,
                         session: Session = Depends(get_db_session)):
    authed_user: UserModel = request.state.user
    return UserRepository.update_user(session, authed_user.id, update_data)


@router.patch("/profile/", response_model=UserDetails, status_code=200)
@authenticate
async def partial_update_profile(request: Request,
                                 partial_update_data: UserPartialUpdate,
                                 session: Session = Depends(get_db_session)):
    authed_user: UserModel = request.state.user
    return UserRepository.partial_update_user(session, authed_user.id, partial_update_data)


@router.delete("/profile/")
@authenticate
async def delete_profile(request: Request,
                         session: Session = Depends(get_db_session)):
    authed_user: UserModel = request.state.user
    is_deleted = UserRepository.delete_user(session, authed_user.id)

    if is_deleted:
        return JSONResponse(content={"details": "User deleted successfully."}, status_code=200)

    raise DeleteUserException()
