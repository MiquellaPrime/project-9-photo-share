from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status

from src.constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, TOKEN_TYPE_FIELD
from src.core.config import settings
from src.core.models import UserOrm
from src.schemas import TokenData


class TokenService:

    def create_access_token(self, user: UserOrm) -> str:
        payload = {
            "sub": user.id,
            "user_id": user.id,
            "role": user.role,
            "token_type": ACCESS_TOKEN_TYPE,
        }
        expire_delta = timedelta(minutes=settings.jwt.access_token_expire_minutes)
        return self._create_jwt(payload, expire_delta=expire_delta)

    def create_refresh_token(self, user: UserOrm) -> str:
        payload = {
            "sub": user.id,
            "user_id": user.id,
            "token_type": REFRESH_TOKEN_TYPE,
        }
        expire_delta = timedelta(days=settings.jwt.refresh_token_expire_days)
        return self._create_jwt(payload, expire_delta=expire_delta)

    def decode_token(self, token: str, token_type: str) -> TokenData:
        try:
            payload = self._decode_jwt(token)
            if payload.get(TOKEN_TYPE_FIELD) != token_type:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid token type",
                )
            user_id = payload.get("user_id")
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token payload",
                )
            role = payload.get("role")
            return TokenData(user_id=user_id, role=role)
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

    def _create_jwt(self, payload: dict, expire_delta: timedelta) -> str:
        to_encode = payload.copy()
        now = datetime.now(timezone.utc)
        expire = now + expire_delta
        to_encode.update({"iat": now, "exp": expire})
        return self._encode_jwt(to_encode)

    def _encode_jwt(self, payload: dict) -> str:
        return jwt.encode(
            payload, settings.jwt.secret, algorithm=settings.jwt.algorithm
        )

    def _decode_jwt(self, token: str) -> dict:
        return jwt.decode(
            token, settings.jwt.secret, algorithms=[settings.jwt.algorithm]
        )
