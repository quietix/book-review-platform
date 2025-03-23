from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from repositories import UserRepository

from utils.db_utils import get_db_session
from utils.auth_utils import create_access_token
from utils.security_utils import verify_password
from schemas import UserDetails, UserUpsert


router = APIRouter()


@router.post("/login")
async def login(db: Session = Depends(get_db_session),
                form_data: OAuth2PasswordRequestForm = Depends()):
    user = UserRepository.retrieve_user_by_username(db, form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", response_model=UserDetails, status_code=201)
async def register(user: UserUpsert,
                   session: Session = Depends(get_db_session)):
    return UserRepository.create_user(session, user)
