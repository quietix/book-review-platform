from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from utils import get_db_session
from repositories import UserRepository
from excepitons import DeleteUserException

from schemas import (
    UserPreview,
    UserDetails,
    UserUpsert,
    UserPartialUpdate,
)


router = APIRouter()


@router.get("/users", response_model=list[UserPreview])
def list_users(session: Session = Depends(get_db_session)):
    return UserRepository.list_users(session)


@router.get("/users/{user_id}", response_model=UserDetails)
def retrieve_user(user_id: int, session: Session = Depends(get_db_session)):
    return UserRepository.retrieve_user(session, user_id)


@router.post("/users", response_model=UserDetails, status_code=201)
def create_user(user: UserUpsert, session: Session = Depends(get_db_session)):
    return UserRepository.create_user(session, user)


@router.put("/users/{user_id}", response_model=UserDetails, status_code=200)
def update_user(user_id: int, user: UserUpsert, session: Session = Depends(get_db_session)):
    return UserRepository.update_user(session, user_id, user)


@router.patch("/users/{user_id}", response_model=UserDetails, status_code=200)
def partial_update_user(user_id: int,
                        user: UserPartialUpdate,
                        session: Session = Depends(get_db_session)):
    return UserRepository.partial_update_user(session, user_id, user)


@router.delete("/users/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_db_session)):
    is_deleted = UserRepository.delete_user(session, user_id)

    if is_deleted:
        return Response("User deleted successfully.", status_code=200)

    raise DeleteUserException()
