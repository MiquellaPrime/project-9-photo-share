from pydantic import BaseModel


class TokenData(BaseModel):
    user_id: int
    role: str | None = None


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"
