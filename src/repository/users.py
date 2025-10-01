from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.users import UserOrm
from src.schemas.enums import UserRoles
from src.schemas.users import UserCreateDto


async def create_user(session: AsyncSession, body: UserCreateDto) -> UserOrm:
    user = UserOrm(
        email=body.email,
        hashed_password=body.password,
        role=UserRoles.USER,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> UserOrm | None:
    search = select(UserOrm).where(UserOrm.id == user_id)
    result = await session.execute(search)
    return result.scalar_one_or_none()


async def get_user_by_email(session: AsyncSession, email: str) -> UserOrm | None:
    search = select(UserOrm).where(UserOrm.email == email)
    result = await session.execute(search)
    return result.scalar_one_or_none()
