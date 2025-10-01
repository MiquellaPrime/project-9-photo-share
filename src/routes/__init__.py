from fastapi import APIRouter

from .photos import router as photos_router

router = APIRouter(prefix="/photos", tags=["photos"])

router.include_router(photos_router)
