from typing import Annotated
from uuid import UUID, uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Path,
    Query,
    UploadFile,
    status,
)

from src.core import cloudinary_cli
from src.core.models import PhotoOrm
from src.dependencies import db_dependency, limit_param, offset_param, user_dependency
from src.repository import photos_crud
from src.schemas import (
    PhotoCreateDto,
    PhotoDto,
    PhotoTransformedDto,
    PhotoUpdateDto,
    TagsParam,
    TransformRequest,
)
from src.services import photos_service

router = APIRouter(prefix="/photos", tags=["photos"])


async def photo_by_uuid(
    session: db_dependency,
    user: user_dependency,
    photo_uuid: Annotated[UUID, Path()],
) -> PhotoOrm:
    """Dependency resolver: returns PhotoOrm by path UUID or raises 404."""
    photo = await photos_crud.get_photo_by_uuid(
        session=session,
        photo_uuid=photo_uuid,
        owner_id=user.id,
    )
    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Photo '{photo_uuid}' not found",
        )
    return photo


photo_orm_dependency = Annotated[PhotoOrm, Depends(photo_by_uuid)]


@router.post(
    "/upload",
    response_model=PhotoDto,
    status_code=status.HTTP_201_CREATED,
)
async def upload_photo(
    session: db_dependency,
    user: user_dependency,
    file: Annotated[UploadFile, File()],
    tags: Annotated[TagsParam, Query()],
    description: Annotated[str | None, Form(min_length=1, max_length=255)] = None,
):
    photo_uuid = uuid4()
    upload_result = await cloudinary_cli.upload_image(
        photo_uuid=photo_uuid,
        file=file.file,
        user_id=user.id,
    )
    photo_create = PhotoCreateDto(
        uuid=photo_uuid,
        owner_id=user.id,
        cloudinary_url=upload_result.secure_url,
        description=description,
    )
    return await photos_service.create_photo_with_tags(
        session=session,
        photo_create=photo_create,
        tags_param=tags,
    )


@router.post(
    "/{photo_uuid}/transform",
    response_model=PhotoTransformedDto,
    status_code=status.HTTP_201_CREATED,
)
async def create_photo_transformation(
    session: db_dependency,
    photo_orm: photo_orm_dependency,
    transformations: TransformRequest,
):
    transformed_url = cloudinary_cli.transform_image(
        photo_uuid=photo_orm.uuid,
        transformations=transformations,
    )
    transformed = await photos_crud.create_transformed_photo(
        session=session,
        photo_orm=photo_orm,
        transformed_url=transformed_url,
    )
    return transformed


@router.get("", response_model=list[PhotoDto])
async def get_all_photos(
    session: db_dependency,
    user: user_dependency,
    offset: offset_param = 0,
    limit: limit_param = 10,
):
    photos = await photos_crud.get_photos(
        session=session,
        owner_id=user.id,
        offset=offset,
        limit=limit,
    )
    return photos


@router.get("/{photo_uuid}", response_model=PhotoDto)
async def get_photo_by_uuid(
    photo_orm: photo_orm_dependency,
):
    return photo_orm


@router.put("/{photo_uuid}", response_model=PhotoDto)
async def update_photo(
    session: db_dependency,
    photo_orm: photo_orm_dependency,
    photo_update: PhotoUpdateDto,
):
    photo = await photos_crud.update_photo(
        session=session,
        photo_orm=photo_orm,
        body=photo_update,
    )
    return photo


@router.delete("/{photo_uuid}")
async def delete_photo(
    session: db_dependency,
    photo_orm: photo_orm_dependency,
):
    await cloudinary_cli.destroy_image(photo_uuid=photo_orm.uuid)
    await photos_crud.delete_photo(session=session, photo_orm=photo_orm)
