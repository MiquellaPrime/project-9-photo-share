from typing import Annotated, Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.cloudinary import cloudinary_cli
from src.core.database import db_helper
from src.core.models.photos import PhotoOrm
from src.core.models.tags import TagOrm
from src.repository import photos as photos_crud
from src.schemas import PhotoCreateDTO, PhotoDTO
from src.schemas.tags import TagCreateDTO, TagDTO

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}

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
    tag: Annotated[Optional[str], Form()] = None,
):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only image files (jpg, png, webp) are allowed",
        )

    photo_uuid = uuid4()
    file_bytes = await file.read()

    upload_result = await cloudinary_cli.upload_image(
        photo_uuid=photo_uuid,
        file=file_bytes,
    )

    tag_list = tag.split(",") if tag else []

    photo_create = PhotoCreateDTO(
        uuid=photo_uuid,
        filename=file.filename,
        cloudinary_url=upload_result.secure_url,
        description=description or None,
        tags=[TagCreateDTO(name=t.strip()) for t in tag_list],
    )

    new_photo = PhotoOrm(
        uuid=photo_create.uuid,
        cloudinary_url=photo_create.cloudinary_url,
        description=photo_create.description,
    )

    for tag_dto in photo_create.tags:
        tag_name = tag_dto.name.strip().lower()
        tag_obj = await session.scalar(select(TagOrm).where(TagOrm.name == tag_name))
        if not tag_obj:
            tag_obj = TagOrm(name=tag_name)
            session.add(tag_obj)
            await session.flush()
        new_photo.tags.append(tag_obj)

    session.add(new_photo)
    await session.commit()
    await session.refresh(new_photo)

    return PhotoDTO(
        uuid=new_photo.uuid,
        cloudinary_url=new_photo.cloudinary_url,
        description=new_photo.description,
        created_at=new_photo.created_at,
        updated_at=new_photo.updated_at,
        tags=[
            TagDTO(
                uuid=t.uuid,
                name=t.name,
                created_at=t.created_at,
                updated_at=t.updated_at,
            )
            for t in new_photo.tags
        ],
    )


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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found"
        )
    return photo
