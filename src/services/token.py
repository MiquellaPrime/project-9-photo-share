from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import HTTPException, status
from jwt import InvalidTokenError

from src.constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, TOKEN_TYPE_FIELD
from src.core import settings
from src.core.models import UserOrm
from src.schemas import TokenData


class TokenService:
    def create_access_token(self, user: UserOrm) -> str:
        """Create access token based on user data."""
        payload = {
            "sub": user.email,
            "user_id": user.id,
            "role": user.role,
        }
        return self._create_jwt(ACCESS_TOKEN_TYPE, payload)

    def create_refresh_token(self, user: UserOrm) -> str:
        """Create refresh token based on user data."""
        payload = {
            "sub": user.email,
            "user_id": user.id,
        }
        expire_delta = timedelta(days=settings.jwt.refresh_token_expire_days)
        return self._create_jwt(REFRESH_TOKEN_TYPE, payload, expire_delta)

    def decode_token(self, token: str, token_type: str) -> TokenData:
        """Decode token and return payload."""
        try:
            payload = self._decode_jwt(token)
            if payload[TOKEN_TYPE_FIELD] != token_type:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid token type",
                )
            return TokenData(**payload)

        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

    def _create_jwt(
        self,
        token_type: str,
        payload: dict[str, Any],
        expire_delta: timedelta | None = None,
    ) -> str:
        """Create JWT token with specified type and expiration delta."""
        payload.update({"token_type": token_type})
        return self._encode_jwt(payload, expire_delta)

    def _encode_jwt(
        self,
        payload: dict[str, Any],
        expire_delta: timedelta | None = None,
    ) -> str:
        """Encode JWT token with additional keys exp and iat."""
        to_encode = payload.copy()
        now = datetime.now(timezone.utc)
        if expire_delta:
            expire = now + expire_delta
        else:
            expire = now + timedelta(minutes=settings.jwt.access_token_expire_minutes)
        to_encode.update({"exp": expire, "iat": now})

        return jwt.encode(
            to_encode,
            key=settings.jwt.secret,
            algorithm=settings.jwt.algorithm,
        )

    def _decode_jwt(self, token: str) -> dict[str, Any]:
        """Decode JWT token and return payload."""
        return jwt.decode(
            token,
            key=settings.jwt.secret,
            algorithms=[settings.jwt.algorithm],
        )
