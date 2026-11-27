from abc import ABC, abstractmethod
from uuid import UUID

from app.models.notification import Notification


class NotiRepository(ABC):

    @abstractmethod
    async def save(
        self,
        notification: Notification,
    ) -> Notification:
        pass

    @abstractmethod
    async def find_by_id_and_user_id(
        self,
        noti_id: UUID,
        user_id: UUID,
    ) -> Notification | None:
        pass

    @abstractmethod
    async def get_by_user_id(
        self,
        user_id: UUID,
    ) -> list[Notification]:
        pass

    @abstractmethod
    async def delete(
        self,
        notification: Notification,
    ) -> None:
        pass
