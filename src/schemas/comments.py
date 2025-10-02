from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CommentBaseDto(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


class CommentCreateDto(CommentBaseDto):
    photo_uuid: UUID


class CommentUpdateDto(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


class CommentDto(CommentBaseDto):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    photo_uuid: UUID
    user_id: int
    created_at: datetime
    updated_at: datetime