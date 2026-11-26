import uuid


from datetime import datetime
from sqlalchemy import DateTime, func, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from sqlalchemy import Enum as SQLEnum
from app.enums.notification_channel import NotificationChannel

class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    titulo: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    contenido: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    canal: Mapped[NotificationChannel] = mapped_column(
        SQLEnum(
            NotificationChannel,
            name="notification_channel",
            values_callable=lambda enum: [item.value for item in enum],
        ),
        nullable=False,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            name="fk_notifications_user_id"
        ),
        nullable=False,
        index=True,
    )

    destinatario: Mapped[str] = mapped_column(
        String(512),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )