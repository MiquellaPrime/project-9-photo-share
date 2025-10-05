from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.core.models import UserOrm
from src.dependencies import db_dependency, token_service_dependency
from src.repository import users_crud
from src.schemas import TokenInfo, UserCreateDto, UserDto
from src.services import PasswordHashService, auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup",
    response_model=UserDto,
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    session: db_dependency,
    user_create: UserCreateDto,
):

    user = await users_crud.get_user_by_email(
        session=session,
        email=str(user_create.email),
    )
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )
    user_create.password = PasswordHashService().hash(user_create.password)
    return await users_crud.create_user(session, user_create)


@router.post("/login", response_model=TokenInfo)
async def login(
    user: Annotated[UserOrm, Depends(auth_service.authenticate_user)],
    token_service: token_service_dependency,
):
    access_token = token_service.create_access_token(user=user)
    refresh_token = token_service.create_refresh_token(user=user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )
