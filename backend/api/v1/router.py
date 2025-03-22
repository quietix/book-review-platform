from fastapi import APIRouter

from .profiles_api import router as profiles_router
from .auth_api import router as auth_router
from .authors_api import router as authors_router
from .genres_api import router as genres_router
from .books_api import router as books_router
from .ratings_api import router as ratings_router
from .reviews_api import router as reviews_router
from .status_api import router as statuses_router


router = APIRouter(prefix="/v1")

router.include_router(auth_router, tags=["Auth"])
router.include_router(profiles_router, tags=["Profiles"])
router.include_router(authors_router, tags=["Authors"])
router.include_router(genres_router, tags=["Genres"])
router.include_router(books_router, tags=["Books"])
router.include_router(ratings_router, tags=["Ratings"])
router.include_router(reviews_router, tags=["Reviews"])
router.include_router(statuses_router, tags=["Statuses"])
