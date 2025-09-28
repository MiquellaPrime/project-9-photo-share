from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from .enums import UserRole


class UserBase(BaseModel):
    email: str
    role: UserRole
    is_active: bool = True
    is_verified: bool = False


class UserCreateDto(UserBase):
    password: str


class UserUpdateDto(UserBase):
    hashed_password: Optional[str] = None


class UserInDB(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
