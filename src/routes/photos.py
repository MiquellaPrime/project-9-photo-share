from typing import Annotated, Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile
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


@router.post("/upload", response_model=PhotoDTO, status_code=201)
async def upload_photo(
    session: db_dependency,
    file: UploadFile,
    description: Annotated[Optional[str], Form(min_length=1, max_length=255)] = None,
):
    photo_uuid = uuid4()

    upload_result = await cloudinary_cli.upload_image(
        photo_uuid=photo_uuid, file=file.file
    )

    photo_create = PhotoCreateDTO(
        uuid=str(photo_uuid),
        filename=file.filename,
        url=upload_result.url,
        description=description,
    )

    new_photo = await photos_crud.create_photo(session=session, photo=photo_create)

    return new_photo


@router.get("/", response_model=list[PhotoDTO])
async def get_photos(
    session: db_dependency,
    offset: int = 0,
    limit: int = 10,
):

    photos = await photos_crud.get_photos(session=session, offset=offset, limit=limit)
    return photos


@router.get("/{photo_uuid}", response_model=PhotoDTO)
async def get_photo(
    session: db_dependency,
    photo_uuid: UUID,
):
    photo = await photos_crud.get_photo_by_uuid(session=session, photo_uuid=photo_uuid)

    if photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo
