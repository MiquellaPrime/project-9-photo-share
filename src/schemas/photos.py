from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.tags import TagCreateDTO, TagDTO


class PhotoBaseDto(BaseModel):
    uuid: UUID
    cloudinary_url: str
    description: str | None = Field(None, min_length=1, max_length=255)


class PhotoCreateDTO(PhotoBaseDto):
    tags: list[TagCreateDTO] = []


class PhotoDTO(PhotoBaseDto):
    model_config = ConfigDict(from_attributes=True)

    created_at: datetime
    updated_at: datetime
    tags: List[TagDTO] = []
