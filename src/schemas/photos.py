from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseModelWithConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PhotoBaseDto(BaseModelWithConfig):
    uuid: UUID
    cloudinary_url: str
    description: str | None = None


class PhotoCreateDto(PhotoBaseDto):
    pass


class PhotoDto(PhotoBaseDto):
    created_at: datetime
    updated_at: datetime
