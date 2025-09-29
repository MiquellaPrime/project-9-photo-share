from typing import Annotated

from fastapi import Depends, Form, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import db_helper, settings
from src.core.models import UserOrm
from src.repository import users as users_crud
from src.services import PasswordHashService, TokenService

# local dependency annotations
db_dependency = Annotated[AsyncSession, Depends(db_helper.session_getter)]
creds_dependency = Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]


async def authenticate_user(
    session: db_dependency,
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form(min_length=6)],
) -> UserOrm:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid email or password",
    )
    if not (user := await users_crud.get_user_by_email(session, str(email))):
        raise unauthed_exc

    if not PasswordHashService().verify(password, user.hashed_password):
        raise unauthed_exc

    return user


async def user_from_refresh(
    session: db_dependency,
    credentials: creds_dependency,
    token_service: Annotated[TokenService, Depends(TokenService)],
) -> UserOrm:
    token_data = token_service.decode_token(
        token=credentials.credentials,
        token_type=settings.jwt.refresh_token_type,
    )
    if not (user := await users_crud.get_user_by_id(session, token_data.user_id)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user",
        )
    return user
