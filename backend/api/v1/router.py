from fastapi import APIRouter

from .profiles_api import router as profiles_router
from .auth_api import router as auth_router


router = APIRouter(prefix="/v1")

router.include_router(profiles_router, tags=["Profiles"])
router.include_router(auth_router, tags=["Auth"])
