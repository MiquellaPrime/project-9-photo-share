from typing import Annotated

from fastapi import Depends, Form, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import db_helper
from src.core.models import UserOrm
from src.repository import users as users_crud
from src.services import PasswordHashService, TokenService

# local dependency annotations
db_dependency = Annotated[AsyncSession, Depends(db_helper.session_getter)]
creds_dependency = Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]
token_service_dependency = Annotated[TokenService, Depends(TokenService)]


def get_current_user(token_type: str):

    async def dependency(
        session: db_dependency,
        credentials: creds_dependency,
        token_service: token_service_dependency,
    ) -> UserOrm:
        token_data = token_service.decode_token(
            token=credentials.credentials,
            token_type=token_type,
        )
        if not (user := await users_crud.get_user_by_id(session, token_data.user_id)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user",
            )
        return user

    return dependency


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


# async def verify_active_user(
#     user: Annotated[
#         UserOrm,
#         Depends(get_current_user(token_type=settings.jwt.access_token_type)),
#     ],
# ) -> UserOrm:
#     """Checks that the user is active."""
#     if not user.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Inactive user",
#         )
#     return user
