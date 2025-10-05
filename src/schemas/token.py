from pydantic import BaseModel

from .enums import UserRoles


class TokenData(BaseModel):
    user_id: int
    role: UserRoles | None = None


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
