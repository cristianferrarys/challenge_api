import logging
import re

from app.models.notification import Notification
from app.strategies.notification_strategy import (
    NotificationStrategy,
)

logger = logging.getLogger(__name__)

class PushStrategy(NotificationStrategy):
    @property
    def channel(self) -> str:
        return "push"

    async def send(
        self,
        notification: Notification,
    ) -> None:

        token = notification.destinatario

        if not re.fullmatch(
            r"[A-Za-z0-9_:\-]{20,512}",
            token,
        ):
            raise ValueError("Invalid device token")

        payload = {
            "token": token,
            "notification": {
                "title": notification.titulo,
                "body": notification.contenido,
            },
            "data": {
                "notification_id": str(notification.id),
            },
        }

        logger.info(
            "Push payload prepared: notification_id=%s",
            payload["data"]["notification_id"],
        )

        logger.info(
            "Push simulated: notification_id=%s, status=SENT",
            notification.id,
        )
