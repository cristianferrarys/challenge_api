import logging
import re
from datetime import datetime, timezone
from app.models.notification import Notification
from app.strategies.notification_strategy import (
    NotificationStrategy,
)
from app.core.exceptions import InvalidRecipientError

logger = logging.getLogger(__name__)

class SMSStrategy(NotificationStrategy):

    @property
    def channel(self) -> str:
        return "sms"

    async def send(
        self,
        notification: Notification,
    ) -> None:

        if not re.fullmatch(
            r"\+[1-9]\d{7,14}",
            notification.destinatario,
        ):
            raise InvalidRecipientError("Numero invalido")

        if len(notification.contenido) > 160:
            raise InvalidRecipientError(
                "SMS tiene mas de  160 characteres"
            )

        sent_at = datetime.now(timezone.utc)

        logger.info(
            "SMS simulated: recipient=%s, sent_at=%s",
            notification.destinatario,
            sent_at,
        )