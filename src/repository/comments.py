from uuid import UUID

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import CommentOrm
from src.schemas import CommentCreateDto, CommentUpdateDto


async def create_comment(
    session: AsyncSession, body: CommentCreateDto, user_id: int
) -> CommentOrm:
    """Create and persist a comment record."""
    comment = CommentOrm(
        photo_uuid=body.photo_uuid,
        user_id=user_id,
        text=body.text,
    )
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return comment


async def get_comments_by_photo(
    session: AsyncSession,
    photo_uuid: UUID,
    offset: int = 0,
    limit: int = 10,
) -> list[CommentOrm]:
    """Return a page of comments for a photo ordered by created_at ASC."""
    stmt = (
        select(CommentOrm)
        .where(CommentOrm.photo_uuid == photo_uuid)
        .order_by(CommentOrm.created_at.asc())
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_comment_by_uuid(
    session: AsyncSession,
    comment_uuid: UUID,
) -> CommentOrm | None:
    """Fetch a single comment by UUID."""
    stmt = select(CommentOrm).where(CommentOrm.uuid == comment_uuid)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def update_comment(
    session: AsyncSession,
    comment_uuid: UUID,
    body: CommentUpdateDto,
) -> CommentOrm | None:
    """Update a comment's text."""
    stmt = (
        update(CommentOrm)
        .where(CommentOrm.uuid == comment_uuid)
        .values(text=body.text)
        .returning(CommentOrm)
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.scalar_one_or_none()


async def delete_comment(
    session: AsyncSession,
    comment_uuid: UUID,
) -> bool:
    """Delete a comment by UUID. Returns True if deleted, False if not found."""
    stmt = delete(CommentOrm).where(CommentOrm.uuid == comment_uuid)
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0


async def count_comments_by_photo(
    session: AsyncSession,
    photo_uuid: UUID,
) -> int:
    """Count total comments for a photo."""
    from sqlalchemy import func
    
    stmt = select(func.count(CommentOrm.uuid)).where(CommentOrm.photo_uuid == photo_uuid)
    result = await session.execute(stmt)
    return result.scalar() or 0