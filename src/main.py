import uvicorn
from fastapi import status
from fastapi.responses import JSONResponse, RedirectResponse

from src.core import settings
from src.create_app import create_app
from src.routes import router as main_router
from src.schemas import HealthResponse

app = create_app()
app.include_router(main_router)


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(
        url="/docs",
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )


@app.get("/health", response_model=HealthResponse, tags=["meta"])
async def check_health():
    return JSONResponse(
        content={"status": "ok"},
        status_code=status.HTTP_200_OK,
        headers={"Cache-Control": "no-cache"},
    )


if __name__ == "__main__":
    uvicorn.run(
        app="src.main:app",
        host=settings.server.host,
        port=settings.server.port,
        reload=settings.server.reload,
    )
