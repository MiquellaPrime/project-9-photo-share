from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.core import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # startup
    yield
    # shutdown
    await db_helper.dispose()


def create_app() -> FastAPI:
    app = FastAPI()
    return app
