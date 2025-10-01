from fastapi import APIRouter

from . import photos as photos_router

router = APIRouter(prefix="/api")

router.include_router(photos_router)
