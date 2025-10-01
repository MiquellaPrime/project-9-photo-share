from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import PhotoOrm
from src.schemas import PhotoCreateDTO


async def create_photo(session: AsyncSession, body: PhotoCreateDTO) -> PhotoOrm:
    """Create and persist a photo record."""
    photo = PhotoOrm(
        uuid=body.uuid,
        cloudinary_url=body.cloudinary_url,
        description=body.description,
    )
    session.add(photo)
    await session.commit()
    return photo


async def get_photos(
    session: AsyncSession,
    offset: int = 0,
    limit: int = 10,
) -> list[PhotoOrm]:
    """Return a page of photos ordered by newest first."""
    stmt = (
        select(PhotoOrm)
        .order_by(PhotoOrm.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_photo_by_uuid(
    session: AsyncSession,
    photo_uuid: UUID,
) -> PhotoOrm | None:
    """Fetch a single photo by UUID."""
    stmt = select(PhotoOrm).where(PhotoOrm.uuid == photo_uuid)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def update_photo_description(
    session: AsyncSession, photo_uuid: UUID, description: str
) -> PhotoOrm | None:
    stmt = (
        update(PhotoOrm)
        .where(PhotoOrm.uuid == photo_uuid)
        .values(description=description)
        .returning(PhotoOrm)
    )
    result = await session.execute(stmt)
    await session.commit()
    update_photo = result.scalar_one_or_none()
    return update_photo


async def delete_photo(session: AsyncSession, photo_uuid: UUID) -> None:
    stmt = delete(PhotoOrm).where(PhotoOrm.uuid == photo_uuid)
    await session.execute(stmt)
    await session.commit()
