from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from .tags import TagsDto


class BaseModelWithConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PhotoTransformedDto(BaseModelWithConfig):
    uuid: UUID
    transformed_url: str
    created_at: datetime


class PhotoBaseDto(BaseModelWithConfig):
    uuid: UUID
    owner_id: int
    cloudinary_url: str
    description: str | None = None


class PhotoCreateDto(PhotoBaseDto):
    pass


class PhotoDto(PhotoBaseDto):
    created_at: datetime
    updated_at: datetime

    tags: list[TagsDto]
    transformations: list[PhotoTransformedDto]


class PhotoUpdateDto(BaseModel):
    description: str | None = Field(default=None, min_length=1, max_length=255)
