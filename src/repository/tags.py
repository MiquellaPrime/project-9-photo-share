from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import TagOrm


async def get_tags_by_names(
    session: AsyncSession,
    names: list[str],
) -> list[TagOrm]:
    """Fetch tags by list of names."""
    stmt = select(TagOrm).where(TagOrm.name.in_(names))

    results = await session.execute(stmt)
    return list(results.scalars().all())
