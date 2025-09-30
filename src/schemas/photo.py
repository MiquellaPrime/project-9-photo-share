from uuid import UUID

from pydantic import BaseModel, Field


class PhotoCreateDTO(BaseModel):
    uuid: UUID
    cloudinary_url: str
    description: str | None = Field(None, min_length=1, max_length=255)
