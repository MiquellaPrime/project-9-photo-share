from fastapi import APIRouter

router = APIRouter()


@router.get("/photos")
async def get_photos():
    return {"message": "Aquí irán tus fotos"}