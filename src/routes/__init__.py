from fastapi import APIRouter

from .auth import router as auth_router
from .photos import router as photos_router

router = APIRouter(prefix="/api")

router.include_router(auth_router)
router.include_router(photos_router)
