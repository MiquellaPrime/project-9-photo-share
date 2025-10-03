from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import PhotoOrm
from src.schemas import PhotoCreateDTO


async def create_photo(session: AsyncSession, body: PhotoCreateDTO) -> PhotoOrm:
    """Create and persist a photo record."""
    photo = PhotoOrm(
        uuid=body.uuid,
        cloudinary_url=body.cloudinary_url,
        cloudinary_id=body.cloudinary_id,
        description=body.description,
    )
    session.add(photo)
    await session.commit()
    await session.refresh(photo)
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
    session: AsyncSession, photo: PhotoOrm, description: str
) -> PhotoOrm:
    photo.description = description
    await session.commit()
    await session.refresh(photo)
    return photo


async def delete_photo(session: AsyncSession, photo: PhotoOrm) -> None:
    await session.delete(photo)
    await session.commit()
