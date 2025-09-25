from fastapi import APIRouter

router = APIRouter()

# Ejemplo de endpoint
@router.get("/photos")
async def get_photos():
    return {"message": "Aquí irán tus fotos"}