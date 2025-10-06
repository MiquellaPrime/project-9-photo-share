from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status

from src.core import cloudinary_cli
from src.core.models import PhotoOrm, UserOrm
from src.dependencies import db_dependency, limit_param, offset_param
from src.repository import photos_crud
from src.schemas import PhotoDto, PhotoUpdateDto, UserRoles
from src.services import auth_service

router = APIRouter(prefix="/photos")


async def photo_by_uuid(
    session: db_dependency,
    photo_uuid: Annotated[UUID, Path()],
) -> PhotoOrm:
    """Dependency resolver: returns PhotoOrm by path UUID or raises 404."""
    photo = await photos_crud.get_photo_by_uuid(
        session=session,
        photo_uuid=photo_uuid,
    )
    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Photo '{photo_uuid}' not found",
        )
    return photo


photo_orm_dependency = Annotated[PhotoOrm, Depends(photo_by_uuid)]
admin_permission = Annotated[
    UserOrm,
    Depends(auth_service.user_with_role(roles={UserRoles.ADMIN})),
]


@router.get("/user/{user_id}", response_model=list[PhotoDto])
async def get_user_photos(
    user: admin_permission,
    session: db_dependency,
    user_id: int,
    offset: offset_param = 0,
    limit: limit_param = 10,
):
    photos = await photos_crud.get_photos(
        session=session,
        owner_id=user_id,
        offset=offset,
        limit=limit,
    )
    return photos


@router.put("/{photo_uuid}", response_model=PhotoDto)
async def update_user_photo(
    user: admin_permission,
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
async def delete_user_photo(
    user: admin_permission,
    session: db_dependency,
    photo_orm: photo_orm_dependency,
):
    await cloudinary_cli.destroy_image(photo_uuid=photo_orm.uuid)
    await photos_crud.delete_photo(session=session, photo_orm=photo_orm)
