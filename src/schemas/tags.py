from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, validator


class TagBaseDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)


class TagCreateDTO(TagBaseDTO):
    @validator("name")
    def normalize_name(cls, v: str) -> str:
        return v.strip().lower()


class TagDTO(TagBaseDTO):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    created_at: datetime
    updated_at: datetime
