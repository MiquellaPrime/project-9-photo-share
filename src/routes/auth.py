from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import db_helper
from src.repository.users import create_user, get_user_by_email
from src.schemas.users import UserCreateDto, UserDto
from src.services.security import pwd_context

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserDto, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreateDto,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):

    existing_user = await get_user_by_email(session, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    hashed_password = pwd_context.hash_password(user_data.password)

    new_user = await create_user(
        session, UserCreateDto(email=user_data.email, hashed_password=hashed_password)
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user
