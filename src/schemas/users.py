from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from .enums import UserRole


class UserCreateDto(BaseModel):

    email: EmailStr
    password: str = Field(min_length=6)


class UserDto(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
