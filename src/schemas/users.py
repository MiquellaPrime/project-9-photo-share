from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.schemas import UserRole


class BaseModelWithConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserBaseDto(BaseModelWithConfig):
    pass


class UserDto(UserBaseDto):
    id: int
    email: EmailStr
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserCreateDto(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
