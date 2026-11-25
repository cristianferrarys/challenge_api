from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserRepositoryImpl(UserRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by_id(self, user_id: UUID) -> User | None:
        return await self.session.get(User, user_id)

    async def find_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def find_all(self) -> list[User]:
        stmt = select(User).order_by(User.name)

        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def save(self, user: User) -> User:
        self.session.add(user)

        await self.session.flush()

        return user

    async def delete(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.flush()