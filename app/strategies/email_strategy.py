import logging

from email_validator import (
    validate_email,
    EmailNotValidError,
)
from app.core.exceptions import InvalidRecipientError
from app.models.notification import Notification
from app.strategies.notification_strategy import (
    NotificationStrategy,
)

logger = logging.getLogger(__name__)


class EmailStrategy(NotificationStrategy):

    @property
    def channel(self) -> str:
        return "email"

    async def send(
        self,
        notification: Notification,
    ) -> None:

        try:
            validate_email(
                notification.destinatario,
                check_deliverability=False,
            )
        except EmailNotValidError as exc:
            raise InvalidRecipientError(
                "Invalid email recipient"
            ) from exc

        template = (
            f"<h1>{notification.titulo}</h1>"
            f"<p>{notification.contenido}</p>"
        )
        logger.info(
            "template: %s",
            template,
        )
        logger.info(
            "Email simulated: notification_id=%s",
            notification.id,
        )