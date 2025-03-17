from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from models import User as UserModel
from utils import (
    get_connection_url,
    get_hashed_password
)
from schemas import (
    UserPreview,
    UserUpsert,
    UserDetails
)


app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=get_connection_url())


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.get("/users/", response_model=list[UserPreview])
def list_users():
    users = db.session.query(UserModel).all()
    return users


@app.post("/users/", response_model=UserDetails)
def create_user(user: UserUpsert):
    hashed_password = get_hashed_password(user.password)

    db_user = UserModel(
        **user.model_dump(exclude={"password"}),
        hashed_password=hashed_password
    )

    db.session.add(db_user)
    db.session.commit()

    return db_user
