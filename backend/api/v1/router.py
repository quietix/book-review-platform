from fastapi import APIRouter

from .profiles_api import router as profiles_router
from .auth_api import router as auth_router
from .authors_api import router as authors_router


router = APIRouter(prefix="/v1")

router.include_router(auth_router, tags=["Auth"])
router.include_router(profiles_router, tags=["Profiles"])
router.include_router(authors_router, tags=["Authors"])
