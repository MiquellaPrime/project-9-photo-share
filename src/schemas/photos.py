from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PhotoCreateDTO(BaseModel):
    uuid: UUID
    cloudinary_url: str
    description: str | None = Field(None, min_length=1, max_length=255)


class PhotoDTO(BaseModel):
    uuid: UUID
    cloudinary_url: str
    description: str | None = Field(None, min_length=1, max_length=255)
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
