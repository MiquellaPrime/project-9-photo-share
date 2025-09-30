from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BaseModelWithConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)


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


class PhotoUpdateDto(BaseModel):
    description: str | None = Field(default=None, min_length=1, max_length=255)
