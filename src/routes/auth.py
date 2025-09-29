from fastapi import APIRouter, HTTPException, status

from src.dependencies import db_dependency
from src.repository import users as users_crud
from src.schemas import UserCreateDto, UserDto
from src.services import PasswordHashService

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
    if user is None:
        user_create.password = PasswordHashService().hash(user_create.password)
        return await users_crud.create_user(
            session=session,
            body=user_create,
        )

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="User already exists",
    )
