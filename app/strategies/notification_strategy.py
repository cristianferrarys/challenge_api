from abc import ABC, abstractmethod
from app.models.notification import Notification

class NotificationStrategy(ABC):

    @property
    @abstractmethod
    def channel(self) -> str:
        pass

    @abstractmethod
    async def send(
        self,
        notification: Notification,
    ) -> None:
        pass