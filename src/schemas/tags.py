from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class TagsParam(BaseModel):
    names: list[str] = Field(default_factory=list)

    @field_validator("names")
    @classmethod
    def validate_tags(cls, names: list[str]) -> list[str]:
        unique_names = {name.capitalize() for name in names}
        if len(unique_names) > 5:
            raise ValueError("there can be no more than 5 unique tags")
        return list(sorted(unique_names))


class TagsDto(BaseModel):
    uuid: UUID
    name: str
    created_at: datetime
