from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import PhotoOrm, TagOrm
from src.repository import photos_crud, tags_crud
from src.schemas import PhotoCreateDto, TagsParam


async def create_photo_with_tags(
    session: AsyncSession,
    photo_create: PhotoCreateDto,
    tags_param: TagsParam,
) -> PhotoOrm:
    """Creates a photo and attaches tags to it."""
    tags = await tags_crud.get_tags_by_names(
        session=session,
        names=tags_param.tags,
    )
    tags_map = {t.name: t for t in tags}

    for name in tags_param.tags:
        if name not in tags_map:
            tags.append(TagOrm(name=name))

    return await photos_crud.create_photo(
        session=session,
        body=photo_create,
        tags=tags,
    )
