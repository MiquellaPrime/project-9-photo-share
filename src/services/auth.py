from typing import Annotated

from fastapi import Depends, Form, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import db_helper
from src.core.models import UserOrm
from src.repository import users_crud

from .security import PasswordHashService

# local dependency annotations
db_dependency = Annotated[AsyncSession, Depends(db_helper.session_getter)]


async def authenticate_user(
    session: db_dependency,
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form(min_length=6)],
) -> UserOrm:
    """Validate email and password, returning the user or raising 401."""
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password",
    )
    if not (user := await users_crud.get_user_by_email(session, str(email))):
        raise unauthed_exc

    if not PasswordHashService().verify(password, user.hashed_password):
        raise unauthed_exc

    return user
