from pydantic import BaseModel

from .schemas.enums import UserRoles


class TokenData(BaseModel):
    user_id: int
    role: UserRoles | None = None
