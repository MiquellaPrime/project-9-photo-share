import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from src.core import db_helper, settings
from src.core.models import UserOrm
from src.repository import users_crud
from src.schemas import UserRoles
from src.services import PasswordHashService


async def create_first_admin(session: AsyncSession) -> None:
    """Create admin user in database if admin does not exist."""
    admin_email = settings.first_admin.email
    admin_password = settings.first_admin.password

    user = await users_crud.get_user_by_email(session=session, email=admin_email)

    if user is not None:
        print("Admin user already exists!")
        return

    admin = UserOrm(
        email=admin_email,
        hashed_password=PasswordHashService().hash(admin_password),
        role=UserRoles.ADMIN,
        is_active=True,
        is_verified=True,
    )
    session.add(admin)
    await session.commit()
    print("Admin user created successfully!")


async def main() -> None:
    async with db_helper.session_factory() as session:
        await create_first_admin(session=session)


if __name__ == "__main__":
    asyncio.run(main())
