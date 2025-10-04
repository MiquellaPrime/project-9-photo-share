from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import CommentOrm
from src.schemas import CommentCreateDto, CommentUpdateDto


async def create_comment(
    session: AsyncSession, body: CommentCreateDto, user_id: UUID
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
    comment: CommentOrm,
    body: CommentUpdateDto,
) -> CommentOrm:
    """Update a comment's text using ORM style."""
    # Update using ORM style
    comment.text = body.text
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return comment


async def update_comment_by_uuid(
    session: AsyncSession,
    comment_uuid: UUID,
    body: CommentUpdateDto,
) -> CommentOrm | None:
    """Update a comment's text by UUID using ORM style."""
    # Get the comment object first
    comment = await get_comment_by_uuid(session, comment_uuid)
    if comment is None:
        return None
    
    return await update_comment(session, comment, body)


async def delete_comment(
    session: AsyncSession,
    comment: CommentOrm,
) -> None:
    """Delete a comment using ORM style."""
    # Delete using ORM style
    await session.delete(comment)
    await session.commit()


async def delete_comment_by_uuid(
    session: AsyncSession,
    comment_uuid: UUID,
) -> bool:
    """Delete a comment by UUID using ORM style. Returns True if deleted, False if not found."""
    # Get the comment object first
    comment = await get_comment_by_uuid(session, comment_uuid)
    if comment is None:
        return False
    
    await delete_comment(session, comment)
    return True


async def count_comments_by_photo(
    session: AsyncSession,
    photo_uuid: UUID,
) -> int:
    """Count total comments for a photo."""
    from sqlalchemy import func
    
    stmt = select(func.count(CommentOrm.uuid)).where(CommentOrm.photo_uuid == photo_uuid)
    result = await session.execute(stmt)
    return result.scalar() or 0