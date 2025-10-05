from fastapi import APIRouter

<<<<<<< Updated upstream
router = APIRouter(prefix="/api")
=======
from .auth import router as auth_router
from .comments import router as comments_router
from .photos import router as photos_router

router = APIRouter(prefix="/api")

router.include_router(auth_router)
router.include_router(photos_router)
router.include_router(comments_router)
>>>>>>> Stashed changes
