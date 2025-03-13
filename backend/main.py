from fastapi import FastAPI, Depends
from fastapi_sqlalchemy import DBSessionMiddleware, db

from sqlmodel import Session, select

from models import User as UserModel
from utils import init_db, get_connection_url
from schemas import (
    UserPreview,
    UserCreate,
    UserDetails
)
from services import UserService


app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=get_connection_url())


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.get("/users", response_model=list[UserPreview])
def list_users():
    users = db.session.execute(select(UserModel)).scalars().all()
    return users


@app.post("/user/", response_model=UserDetails)
def create_user(user: UserCreate):
    hashed_password = UserService.get_hashed_password(user.password)

    db_user = UserModel(
        **user.dict(exclude={"password"}),
        hashed_password=hashed_password
    )

    db.session.add(db_user)
    db.session.commit()

    return db_user
