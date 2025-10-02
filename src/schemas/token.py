from pydantic import BaseModel

from .enums import UserRoles


class TokenData(BaseModel):
    user_id: int
    role: UserRoles | None = None
