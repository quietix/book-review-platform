from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
import jwt as jwt_pac

from fastapi import HTTPException, FastAPI
from fastapi.openapi.utils import get_openapi

from sqlalchemy.orm import Session

from config import config
from repositories import UserRepository
from utils.db_utils import get_db_session
from models import User as UserModel


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.JWT_SECRET_KEY, algorithm=config.AUTH_ALGORITHM)
    return encoded_jwt


def verify_token(token: str, session: Session = None) -> UserModel:
    try:
        if session is None:
            session = next(get_db_session())

        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.AUTH_ALGORITHM])
        username = payload.get("sub")
        user = UserRepository.retrieve_user_by_username(session, username)
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt_pac.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_custom_openapi_schema(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    security_scheme = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    }

    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

    if "securitySchemes" not in openapi_schema["components"]:
        openapi_schema["components"]["securitySchemes"] = {}

    openapi_schema["components"]["securitySchemes"]["BearerAuth"] = security_scheme

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]

    return openapi_schema
