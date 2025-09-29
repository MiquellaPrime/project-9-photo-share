from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import db_helper
from src.core.models.photo import PhotoORM
from src.schemas.photo import PhotoSchema
from src.services.photo_service import transform_photo, upload_photo

router = APIRouter()
get_db = db_helper.session_getter

DbSession = Annotated[AsyncSession, Depends(db_helper.session_getter)]
UploadedFile = Annotated[UploadFile, File(...)]
FormStr = Annotated[Optional[str], Form(None)]


# ------------------------
# GET all photos
# ------------------------
@router.get("/", response_model=List[PhotoSchema])
async def read_photos(db: DbSession):
    result = await db.execute(select(PhotoORM))
    return result.scalars().all()


@router.post("/", response_model=PhotoSchema)
async def create_photo(
    file: UploadFile,  # Uploaded photo file
    description: FormStr,  # Optional photo description
    tags: FormStr,  # Optional photo description
    transformations: FormStr,
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
    result = await db.execute(select(PhotoORM).where(PhotoORM.public_id == public_id))
    return result.scalars().one_or_none()


# ------------------------
# PUT update photo description
# ------------------------
@router.put("/{photo_id}", response_model=PhotoSchema)
async def update_photo(
    photo_id: int,
    description: Annotated[str, Form(...)],
    db: DbSession,
):
    result = await db.execute(select(PhotoORM).where(PhotoORM.id == photo_id))
    photo = result.scalar_one_or_none()
    if photo:
        photo.description = description

    await db.commit()
    await db.refresh(photo)
    return photo


# ------------------------
# DELETE photo by ID
# ------------------------
@router.delete("/{photo_id}")
async def delete_photo(photo_id: int, db: DbSession):
    result = await db.execute(select(PhotoORM).where(PhotoORM.id == photo_id))
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
    result = await db.execute(select(PhotoORM).where(PhotoORM.id == photo_id))
    photo = result.scalar_one_or_none()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    transformed_url = await transform_photo(photo, transformation, db)
    return {"photo": photo, "transformed_url": transformed_url}
