from fastapi import APIRouter

from src.dependencies import user_dependency
from src.schemas import UserDto

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/me", response_model=UserDto)
async def get_me(user: user_dependency):
    return user
