from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status

from src.core.models import CommentOrm, UserOrm
from src.dependencies import db_dependency
from src.repository import comments_crud
from src.schemas import CommentDto, CommentUpdateDto, UserRoles
from src.services import auth_service

router = APIRouter(prefix="/comments")


async def comment_by_uuid(
    session: db_dependency,
    comment_uuid: Annotated[UUID, Path()],
) -> CommentOrm:
    """Dependency resolver: returns CommentOrm by path UUID or raises 404."""
    comment = await comments_crud.get_comment_by_uuid(
        session=session,
        comment_uuid=comment_uuid,
    )
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment '{comment_uuid}' not found",
        )
    return comment


comment_orm_dependency = Annotated[CommentOrm, Depends(comment_by_uuid)]
moderator_or_higher_permission = Annotated[
    UserOrm,
    Depends(auth_service.user_with_role(roles={UserRoles.MODERATOR, UserRoles.ADMIN})),
]


@router.put("/{comment_uuid}", response_model=CommentDto)
async def update_user_comment(
    user: moderator_or_higher_permission,
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


@router.delete("/{comment_uuid}", response_model=CommentDto)
async def delete_user_comment(
    user: moderator_or_higher_permission,
    session: db_dependency,
    comment_orm: comment_orm_dependency,
):
    await comments_crud.delete_comment(session=session, comment_orm=comment_orm)
