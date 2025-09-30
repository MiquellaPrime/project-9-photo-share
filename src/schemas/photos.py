from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PhotoBaseDto(BaseModel):
    uuid: UUID
    cloudinary_url: str
    description: str | None = Field(None, min_length=1, max_length=255)


class PhotoCreateDTO(PhotoBaseDto):
    pass


class PhotoDTO(PhotoBaseDto):
    model_config = ConfigDict(from_attributes=True)

    created_at: datetime
    updated_at: datetime
