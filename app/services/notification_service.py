from abc import ABC, abstractmethod
from uuid import UUID
from app.models.notification import Notification
from app.schemas.notification import NotiCreate, NotiUpdate,NotiResponse

class NotificationService(ABC):
    @abstractmethod
    async def create(self, data: NotiCreate, user_id: UUID) -> Notification:
        pass
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> NotiResponse:
        pass
    @abstractmethod
    async def get_all(self) -> list[Notification]:
        pass

    @abstractmethod
    async def update(
        self,
        user_id: UUID,
        data: NotiUpdate,
    ) -> Notification:
        pass

    @abstractmethod
    async def get_my_notifications(
        self,
        user_id: UUID,
    ) -> list[Notification]:
        pass
    @abstractmethod
    async def delete(self, noti_id: UUID) -> None:
        pass