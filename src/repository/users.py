from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import UserOrm
from src.schemas import UserCreateDto, UserRoles


async def create_user(
    session: AsyncSession,
    body: UserCreateDto,
) -> UserOrm:
    """Create a new user."""
    user = UserOrm(
        email=body.email,
        hashed_password=body.password,
        role=UserRoles.USER,
    )
    session.add(user)
    await session.commit()
    return user


async def get_user_by_id(
    session: AsyncSession,
    user_id: int,
) -> UserOrm:
    """Get a user by id."""
    stmt = select(UserOrm).filter_by(id=user_id)

    result = await session.execute(stmt)
    return result.scalars().first()


async def get_user_by_email(
    session: AsyncSession,
    email: str,
) -> UserOrm | None:
    """Get a user by email."""
    stmt = select(UserOrm).filter_by(email=email)

    result = await session.execute(stmt)
    return result.scalars().first()
