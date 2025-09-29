from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.core import db_helper
from src.routes import photos as photo_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # startup
    yield
    # shutdown
    await db_helper.dispose()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.include_router(photo_router.router, prefix="/api/v1/photos", tags=["photos"])

    return app
