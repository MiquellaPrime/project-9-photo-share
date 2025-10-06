from fastapi import APIRouter

from .comments import router as comments_router
from .photos import router as photos_router

router = APIRouter(prefix="/admin", tags=["admin"])

router.include_router(photos_router)
router.include_router(comments_router)
