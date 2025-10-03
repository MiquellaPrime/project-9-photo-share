from typing import Annotated, Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.cloudinary import cloudinary_cli
from src.core.database import db_helper
from src.repository import photos as photos_crud
from src.schemas import PhotoCreateDTO, PhotoDTO

router = APIRouter(
    prefix="/photos",
    tags=["photos"],
)

db_dependency = Annotated[AsyncSession, Depends(db_helper.session_getter)]


@router.post("/upload", response_model=PhotoDTO, status_code=status.HTTP_201_CREATED)
async def upload_photo(
    session: db_dependency,
    file: UploadFile,
    description: Annotated[Optional[str], Form(min_length=1, max_length=255)] = None,
):
    photo_uuid = uuid4()

    file_bytes = await file.read()

    upload_result = await cloudinary_cli.upload_image(
        photo_uuid=photo_uuid,
        file=file_bytes,
    )
    cloudinary_id = getattr(upload_result, "public_id", str(photo_uuid))

    photo_create = PhotoCreateDTO(
        uuid=photo_uuid,
        filename=file.filename,
        cloudinary_url=upload_result.secure_url,
        cloudinary_id=cloudinary_id,
        description=description or None,
    )

    new_photo = await photos_crud.create_photo(session=session, body=photo_create)

    return new_photo


@router.get("/", response_model=list[PhotoDTO], status_code=status.HTTP_200_OK)
async def get_photos(
    session: db_dependency,
    offset: int = 0,
    limit: int = 10,
):

    photos = await photos_crud.get_photos(session=session, offset=offset, limit=limit)
    return photos


@router.get("/{photo_uuid}", response_model=PhotoDTO, status_code=status.HTTP_200_OK)
async def get_photo(
    session: db_dependency,
    photo_uuid: UUID,
):
    photo = await photos_crud.get_photo_by_uuid(session=session, photo_uuid=photo_uuid)

    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found"
        )
    return photo


@router.delete("/{photo_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_photo(
    session: db_dependency,
    photo_uuid: UUID,
):
    photo = await photos_crud.get_photo_by_uuid(session=session, photo_uuid=photo_uuid)
    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found"
        )
    try:
        destroy_result = await cloudinary_cli.destroy_image(photo.cloudinary_id)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to delete image in Cloudinary",
        ) from exc

    result_value = None
    if isinstance(destroy_result, dict):
        result_value = destroy_result.get("result")
    elif isinstance(destroy_result, str):
        result_value = destroy_result

    if result_value is not None and str(result_value).lower() not in {
        "ok",
        "not_found",
        "not found",
    }:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Cloudinary deletion returned unexpected result: {destroy_result}",
        )
    await photos_crud.delete_photo(session=session, photo=photo)
    return None


@router.put("/{photo_uuid}", response_model=PhotoDTO, status_code=status.HTTP_200_OK)
async def update_photo_description(
    session: db_dependency,
    photo_uuid: UUID,
    description: Annotated[str, Form(min_length=1, max_length=255)],
):
    photo = await photos_crud.get_photo_by_uuid(session=session, photo_uuid=photo_uuid)
    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found"
        )

    updated_photo = await photos_crud.update_photo_description(
        session=session,
        photo=photo,
        description=description,
    )
    return updated_photo
