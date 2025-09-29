from pydantic import BaseModel


class TokenData(BaseModel):
    user_id: int
    role: str | None = None
