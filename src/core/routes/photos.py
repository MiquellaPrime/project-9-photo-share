from typing import Annotated, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import db_helper
from src.core.models.photo import Photo
from src.core.schemas.photo import PhotoSchema
from src.core.services.photo_service import upload_photo

router = APIRouter()

DbSession = Annotated[AsyncSession, Depends(db_helper.session_getter)]
UploadedFile = Annotated[UploadFile, File(...)]
PhotoDescription = Annotated[Optional[str], Form(None)]
PhotoTags = Annotated[Optional[str], Form(None)]
PhotoTransformations = Annotated[Optional[str], Form(None)]


# ------------------------
# GET all photos
# ------------------------
@router.get("/, response_model=[PhotoSchema]")
async def read_photos(db: DbSession):
    result = await db.execute(select(Photo))
    return result.scalars().all()


@router.post("/", response_model=PhotoSchema)
async def create_photo(
    file: UploadFile,  # Uploaded photo file
    description: PhotoDescription,  # Optional photo description
    tags: PhotoTags,  # Optional photo description
    transformations: PhotoTransformations,
    db: DbSession,
    user_id: int = 1,  # This should be from an authenticated user
):
    try:
        return await upload_photo(file, description, tags, transformations, user_id, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ------------------------
# GET photo by public_id
# ------------------------
@router.get("/public/{public_id}", response_model=PhotoSchema)
async def get_photo(public_id: str, db: DbSession):
    result = await db.execute(select(Photo).where(Photo.public_id == public_id))
    return result.scalars_one_or_none()


# ------------------------
# PUT update photo description
# ------------------------
@router.put("/{photo_id}", response_model=PhotoSchema)
async def update_photo(
    photo_id: int,
    description: Annotated[str, Form(...)],
    db: DbSession,
):
    result = await db.execute(select(Photo).where(Photo.id == photo_id))
    photo = result.scalar_one_or_none()
    if photo:
        photo.description = description
    return photo


# ------------------------
# DELETE photo by ID
# ------------------------
@router.delete("/{photo_id}")
async def delete_photo(photo_id: int, db: DbSession):
    result = await db.execute(select(Photo).where(Photo.id == photo_id))
    photo = result.scalar_one_or_none()
    if photo:
        await db.delete(photo)
        await db.commit()
    return {"detail": "Photo delete"}


@router.post("/{photo_id}/transform")
async def apply_transformation(
    photo_id: int,
    transformation: Annotated[str, Form(...)],
    db: DbSession,
):
    result = await db.execute(select(Photo).where(Photo.id == photo_id))
    photo = result.scalar_one_or_none()
    if photo:
        photo.transformations.append(transformation)
    return photo
