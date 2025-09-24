from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(
        url="/docs",
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )
