from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BaseModelWithConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CommentBaseDto(BaseModelWithConfig):
    text: str = Field(min_length=1, max_length=2000)


class CommentDto(CommentBaseDto):
    uuid: UUID
    photo_uuid: UUID
    user_id: int
    created_at: datetime
    updated_at: datetime


class CommentCreateDto(CommentBaseDto):
    pass


class CommentUpdateDto(BaseModel):
    text: str = Field(min_length=1, max_length=2000)
