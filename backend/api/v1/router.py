from fastapi import APIRouter

from .profiles_routes import router as profiles_router
from .auth_routes import router as auth_router
from .authors_routes import router as authors_router
from .genres_routes import router as genres_router
from .books_routes import router as books_router
from .ratings_routes import router as ratings_router
from .reviews_routes import router as reviews_router
from .status_routes import router as statuses_router
from .reading_item_routes import router as reading_item_router


router = APIRouter(prefix="/v1")

router.include_router(auth_router, tags=["Auth"])
router.include_router(profiles_router, tags=["Profiles"])
router.include_router(authors_router, tags=["Authors"])
router.include_router(genres_router, tags=["Genres"])
router.include_router(books_router, tags=["Books"])
router.include_router(ratings_router, tags=["Ratings"])
router.include_router(reviews_router, tags=["Reviews"])
router.include_router(statuses_router, tags=["Statuses"])
router.include_router(reading_item_router, tags=["Reading Items"])
