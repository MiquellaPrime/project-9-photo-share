from __future__ import annotations

from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import PhotoOrm
from src.schemas.photo import PhotoCreateDTO


async def create_photo(session: AsyncSession, body: PhotoCreateDTO) -> PhotoOrm:
    photo = PhotoOrm(
        uuid=body.uuid,
        cloudinary_url=body.cloudinary_url,
        description=body.description,
    )
    session.add(photo)
    await session.flush()
    return photo


async def get_photos(
    session: AsyncSession, offset: int = 0, limit: int = 10
) -> list[PhotoOrm]:
    stmt = (
        select(PhotoOrm).order_by(desc(PhotoOrm.created_at)).offset(offset).limit(limit)
    )

    result = await session.execute(stmt)
    return result.scalars().all()


async def get_photo_by_uuid(session: AsyncSession, photo_uuid: UUID) -> PhotoOrm | None:
    stmt = select(PhotoOrm).where(PhotoOrm.uuid == photo_uuid)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
