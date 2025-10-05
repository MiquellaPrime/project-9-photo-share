from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status

from src.core.models import PhotoOrm, CommentOrm
from src.dependencies import db_dependency, limit_param, offset_param, user_dependency
from src.repository import comments_crud, photos_crud
from src.schemas import CommentCreateDto, CommentDto, CommentUpdateDto

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
)


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


async def comment_by_uuid(
    session: db_dependency,
    user: user_dependency,
    comment_uuid: Annotated[UUID, Path()],
) -> CommentOrm:
    """Dependency resolver: returns CommentOrm by path UUID or raises 404."""
    comment = await comments_crud.get_comment_by_uuid(
        session=session,
        comment_uuid=comment_uuid,
        user_id=user.id,
    )
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment '{comment_uuid}' not found",
        )
    return comment


photo_orm_dependency = Annotated[PhotoOrm, Depends(photo_by_uuid)]
comment_orm_dependency = Annotated[CommentOrm, Depends(comment_by_uuid)]


@router.post(
    "/photo/{photo_uuid}",
    response_model=CommentDto,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    session: db_dependency,
    user: user_dependency,
    photo_orm: photo_orm_dependency,
    comment_create: CommentCreateDto,
):
    comment = await comments_crud.create_comment(
        session=session,
        photo_uuid=photo_orm.uuid,
        user_id=user.id,
        body=comment_create,
    )
    return comment


@router.get("/photo/{photo_uuid}", response_model=list[CommentDto])
async def get_comments_by_photo(
    session: db_dependency,
    user: user_dependency,
    photo_orm: photo_orm_dependency,
    offset: offset_param = 0,
    limit: limit_param = 10,
):
    comments = await comments_crud.get_comments_by_photo(
        session=session,
        photo_uuid=photo_orm.uuid,
        offset=offset,
        limit=limit,
    )
    return comments


@router.get("/comments", response_model=list[CommentDto])
async def get_user_comments(
    session: db_dependency,
    user: user_dependency,
    offset: offset_param = 0,
    limit: limit_param = 10,
):
    comments = await comments_crud.get_comments(
        session=session,
        user_id=user.id,
        offset=offset,
        limit=limit,
    )
    return comments


@router.get("/comment/{comment_uuid}", response_model=CommentDto)
async def get_comment_by_uuid(
    session: db_dependency,
    comment_orm: comment_orm_dependency,
):
    return comment_orm


@router.put("/comment/{comment_uuid}", response_model=CommentDto)
async def update_comment(
    session: db_dependency,
    comment_orm: comment_orm_dependency,
    comment_update: CommentUpdateDto,
):
    comment = await comments_crud.update_comment(
        session=session,
        comment_orm=comment_orm,
        body=comment_update,
    )
    return comment
