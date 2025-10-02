from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status

from src.constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, TOKEN_TYPE_FIELD
from src.core.config import settings
from src.core.models import UserOrm
from src.schemas import TokenData


class TokenService:

    def __init__(self):
        self.secret = settings.jwt.secret
        self.algorithm = settings.jwt.algorithm
        self.access_token_expire_minutes = settings.jwt.access_token_expire_minutes

    def create_access_token(self, user: UserOrm) -> str:
        payload = {
            "sub": user.id,
            "user_id": user.id,
            "role": user.role.value,
            "token_type": ACCESS_TOKEN_TYPE,
        }
        return self._create_jwt(
            payload, expire_minutes=self.access_token_expire_minutes
        )

    def create_refresh_token(self, user: UserOrm) -> str:
        payload = {
            "sub": user.id,
            "user_id": user.id,
            "token_type": REFRESH_TOKEN_TYPE,
        }
        return self._create_jwt(
            payload, expire_minutes=self.access_token_expire_minutes
        )

    def decode_token(self, token: str, token_type: str) -> TokenData:
        try:
            payload = self._decode_jwt(token)
            if payload.get(TOKEN_TYPE_FIELD) != token_type:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Invalid token type. Expected {token_type}",
                )
            user_id = payload.get("user_id")
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token payload",
                )
            role = payload.get("role")
            return TokenData(user_id=user_id, role=role)
        except jwt.InvalidTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Could not validate credentials: {str(e)}",
            )

    def _create_jwt(self, payload: dict, expire_minutes: int) -> str:
        to_encode = payload.copy()
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=expire_minutes)
        to_encode.update({"iat": now, "exp": expire})
        return self._encode_jwt(to_encode)

    def _encode_jwt(self, payload: dict) -> str:
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def _decode_jwt(self, token: str) -> dict:
        return jwt.decode(token, self.secret, algorithms=self.algorithm)
