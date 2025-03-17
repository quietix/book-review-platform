from fastapi import APIRouter
from fastapi_sqlalchemy import db

from repositories import UserRepository

from schemas import (
    UserPreview,
    UserDetails,
    UserUpsert,
    UserPartialUpdate,
)


router = APIRouter()


@router.get("/users", response_model=list[UserPreview])
def list_users():
    return UserRepository.list_users(db.session)


@router.get("/users/{user_id}", response_model=UserDetails)
def retrieve_users(user_id: int):
    return UserRepository.retrieve_user(db.session, user_id)


@router.post("/users", response_model=UserDetails)
def create_user(user: UserUpsert):
    return UserRepository.create_user(db.session, user)


@router.put("/users/{user_id}", response_model=UserDetails)
def update_user(user_id: int, user: UserUpsert):
    return UserRepository.update_user(db.session, user_id, user)


@router.patch("/users/{user_id}", response_model=UserDetails)
def partial_update_user(user_id: int, user: UserPartialUpdate):
    return UserRepository.partial_update_user(db.session, user_id, user)


@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    return UserRepository.delete_user(db.session, user_id)
