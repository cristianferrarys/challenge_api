from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification
from app.repositories.noti_repository import NotiRepository


class NotiRepositoryImpl(NotiRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by_id(self, noti_id: UUID) -> Notification | None:
        return await self.session.get(Notification, noti_id)

    async def find_all(self) -> list[Notification]:
        stmt = select(Notification).order_by(Notification.id)

        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def save(self, noti: Notification) -> Notification:
        self.session.add(noti)

        await self.session.flush()

        return noti

    async def get_by_user_id(
        self,
        user_id: UUID,
    ) -> list[Notification]:
        stmt = (
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())


    async def delete(self, noti: Notification) -> None:
        await self.session.delete(noti)
        await self.session.flush()