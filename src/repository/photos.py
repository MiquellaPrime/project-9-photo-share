from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.models import PhotoOrm, TagOrm
from src.schemas import PhotoCreateDto, PhotoUpdateDto


async def create_photo(
    session: AsyncSession,
    body: PhotoCreateDto,
    tags: list[TagOrm],
) -> PhotoOrm:
    """Create and persist a photo record."""
    photo_orm = PhotoOrm(
        uuid=body.uuid,
        owner_id=body.owner_id,
        cloudinary_url=body.cloudinary_url,
        description=body.description,
        tags=tags,
    )
    session.add(photo_orm)
    await session.commit()
    return photo_orm


async def get_photos(
    session: AsyncSession,
    owner_id: int,
    offset: int = 0,
    limit: int = 10,
) -> list[PhotoOrm]:
    """Return a page of photos ordered by newest first."""
    stmt = (
        select(PhotoOrm)
        .filter_by(owner_id=owner_id)
        .order_by(PhotoOrm.created_at.desc())
        .offset(offset)
        .limit(limit)
        .options(selectinload(PhotoOrm.tags))
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_photo_by_uuid(
    session: AsyncSession,
    photo_uuid: UUID,
    owner_id: int | None = None,
) -> PhotoOrm | None:
    """Fetch a single photo by UUID."""
    stmt = select(PhotoOrm).filter_by(uuid=photo_uuid)
    if owner_id:
        stmt = stmt.filter_by(owner_id=owner_id)

    stmt = stmt.options(selectinload(PhotoOrm.tags))

    result = await session.execute(stmt)
    return result.scalars().first()


async def update_photo(
    session: AsyncSession,
    photo_orm: PhotoOrm,
    body: PhotoUpdateDto,
) -> PhotoOrm:
    """Apply a partial update to an existing photo."""
    photo_orm.description = body.description

    await session.commit()
    await session.refresh(photo_orm)
    return photo_orm


async def delete_photo(
    session: AsyncSession,
    photo_orm: PhotoOrm,
) -> None:
    """Delete a photo."""
    await session.delete(photo_orm)
    await session.commit()
