from functools import wraps

from fastapi import HTTPException, Request

from utils.auth_utils import verify_token


def authenticate(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        authorization = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401,
                                detail="Missing or invalid Authorization header")

        token = authorization.split(" ")[1]

        session = kwargs.get("session")
        user = verify_token(token, session)

        request.state.user = user

        return await func(request, *args, **kwargs)

    return wrapper
