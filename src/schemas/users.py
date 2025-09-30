from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from .enums import UserRoles


class UserBaseDto(BaseModel):
    email: EmailStr


class UserCreateDto(UserBaseDto):
    password: str = Field(min_length=6)


class UserDto(UserBaseDto):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: UserRoles
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
