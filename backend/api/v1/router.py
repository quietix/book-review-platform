from fastapi import APIRouter

from .users_api import router as users_router


router = APIRouter(prefix="/v1")

router.include_router(users_router, tags=["Users"])
