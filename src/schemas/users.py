from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.schemas import UserRole


class BaseModelWithConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserBaseDto(BaseModelWithConfig):
    email: EmailStr


class UserDto(UserBaseDto):
    id: int
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserCreateDto(UserBaseDto):
    password: str = Field(min_length=6)
