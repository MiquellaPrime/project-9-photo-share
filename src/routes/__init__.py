from fastapi import APIRouter

from .comments import router as comments_router

router = APIRouter(prefix="/api")

router.include_router(comments_router)
