from fastapi import status
from fastapi.responses import JSONResponse, RedirectResponse
import uvicorn


from src.core.schemas import HealthResponse
from src.create_app import create_app
from src.core.routes import photos as photo_router

app = create_app()

## Core Routes

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

app.include_router(photo_router.router, prefix="/api/v1/photos", tags=["photos"])

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)