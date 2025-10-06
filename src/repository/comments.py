from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import CommentOrm
from src.schemas import CommentCreateDto, CommentUpdateDto


async def create_comment(
    session: AsyncSession,
    photo_uuid: UUID,
    user_id: int,
    body: CommentCreateDto,
) -> CommentOrm:
    """Create and persist a comment record."""
    comment = CommentOrm(
        photo_uuid=photo_uuid,
        user_id=user_id,
        text=body.text,
    )
    session.add(comment)
    await session.commit()
    return comment


async def get_comments_by_photo(
    session: AsyncSession,
    photo_uuid: UUID,
    offset: int = 0,
    limit: int = 10,
) -> list[CommentOrm]:
    """Return comments for a photo ordered by creation time."""
    stmt = (
        select(CommentOrm)
        .filter_by(photo_uuid=photo_uuid)
        .order_by(CommentOrm.created_at)
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_comments(
    session: AsyncSession,
    user_id: int,
    offset: int = 0,
    limit: int = 10,
) -> list[CommentOrm]:
    """Return user comments."""
    stmt = (
        select(CommentOrm)
        .filter_by(user_id=user_id)
        .order_by(CommentOrm.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_comment_by_uuid(
    session: AsyncSession,
    comment_uuid: UUID,
    user_id: int | None = None,
) -> CommentOrm | None:
    """Fetch a comment by UUID."""
    stmt = select(CommentOrm).filter_by(uuid=comment_uuid)

    if user_id is not None:
        stmt = stmt.filter_by(user_id=user_id)

    result = await session.execute(stmt)
    return result.scalars().first()


async def update_comment(
    session: AsyncSession,
    comment_orm: CommentOrm,
    body: CommentUpdateDto,
) -> CommentOrm:
    """Update an existing comment."""
    comment_orm.text = body.text

    await session.commit()
    await session.refresh(comment_orm)
    return comment_orm


async def delete_comment(
    session: AsyncSession,
    comment_orm: CommentOrm,
) -> None:
    """Delete an existing comment."""
    await session.delete(comment_orm)
    await session.commit()
