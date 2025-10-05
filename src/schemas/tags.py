from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TagsParam(BaseModel):
    tags: list[str] = Field(default_factory=list)

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, tags: list[str]) -> list[str]:
        unique_tags = {tag.capitalize() for tag in tags}
        if len(unique_tags) > 5:
            raise ValueError("there can be no more than 5 unique tags")
        return list(sorted(unique_tags))


class TagsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    name: str
    created_at: datetime
