from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from src.core.database import db_helper
from src.core.models.photo import Photo
from src.core.services.photo_service import upload_photo, transform_photo
from src.core.schemas.photo import PhotoSchema

router = APIRouter()



# ------------------------
# GET all photos
# ------------------------
@router.get("/, response_model=[PhotoSchema]")
async def read_photos(db: AsyncSession = Depends(db_helper.session_getter)):
    result = await db.execute(select(Photo))
    return result.scalars().all()


@router.post("/", response_model=PhotoSchema)
async def update_photo(
        file: UploadFile = File(...), # Uploaded photo file
        description: str = Form(None), # Optional photo description
        tags: str = Form(None), # Optional photo description
        transformations: Optional[str] = Form(None),
        db: AsyncSession = Depends(db_helper.session_getter),
        user_id: int = 1 # This should be from an authenticated user
):
    try:
        return await upload_photo(file, description, tags, transformations, user_id, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ------------------------
# GET photo by public_id
# ------------------------
@router.get("/public/{public_id}")
async def get_photo(public_id: str, db: AsyncSession = Depends(db_helper.session_getter)):
    result = await db.execute(select(Photo).where(Photo.public_id == public_id))
    photo = result.scalar_one_or_none()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo


# ------------------------
# PUT update photo description
# ------------------------
@router.put("/{photo_id}")
async def update_photo(photo_id: int, description: str = Form(...), db: AsyncSession = Depends(db_helper.session_getter)):
    result = await db.execute(select(Photo).where(Photo.id == photo_id))
    photo = result.scalar_one_or_none()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    photo.description = description
    await db.commit()
    await db.refresh(photo)
    return photo


# ------------------------
# DELETE photo by ID
# ------------------------
@router.delete("/{photo_id}")
async def delete_photo(photo_id: int, db: AsyncSession = Depends(db_helper.session_getter)):
    result = await db.execute(select(Photo).where(Photo.id == photo_id))
    photo = result.scalar_one_or_none()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    await transform_photo(photo, "delete", db)
    await db.delete(photo)
    await db.commit()
    return {"detail": "Photo delete"}





@router.post("/{photo_id}/transform")
async def apply_transformation(
        photo_id: int,
        transformation: str = Form(...),
        db:AsyncSession = Depends(db_helper.session_getter)
):
    result = await db.execute(select(Photo).where(Photo.id == photo_id))
    photo = result.scalar_one_or_none()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    try:
        transformed_url = await transform_photo(photo, transformation, db)
        return {"original_url": photo.url, "transformed_url": transformed_url}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


