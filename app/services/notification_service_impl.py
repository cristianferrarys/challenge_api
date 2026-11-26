from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from starlette.concurrency import run_in_threadpool

from app.core.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.models.notification import Notification
from app.repositories.noti_repository import NotiRepository
from app.schemas.notification import NotiCreate, NotiUpdate, NotiResponse
from app.services.notification_service import NotificationService

from app.auth import hash_password


class NotificationServiceImpl(NotificationService):

    def __init__(
        self,
        repository: NotiRepository,
        session: AsyncSession,
    ):
        self.repository = repository
        self.session = session

    async def create(self, data: NotiCreate) -> Notification:
        try:
            async with self.session.begin():
                notification = Notification(
                    titulo=data.titulo,
                    contenido=data.contenido,
                    canal=data.canal,
                )

                await self.repository.save(notification)

            return notification

        except IntegrityError as exc:
            # También protege frente a altas concurrentes.
            raise UserAlreadyExistsError(
                "El email ya está registrado"
            ) from exc

    async def get_by_id(self, noti_id: UUID) -> NotiResponse:
        user = await self.repository.find_by_id(noti_id)

        if user is None:
            raise UserNotFoundError(
                "Notification no encontrado"
            )

        return user

    async def get_all(self) -> list[Notification]:
        return await self.repository.find_all()

    async def update(
        self,
        noti_id: UUID,
        data: NotiUpdate,
    ) -> Notification:
        try:
            async with self.session.begin():
                noti = await self.repository.find_by_id(
                    noti_id
                )

                if noti is None:
                    raise UserNotFoundError(
                        "Notification no encontrado"
                    )

                changes = data.model_dump(
                    exclude_unset=True
                )

                for field, value in changes.items():
                    if value is None:
                        raise ValueError(
                            f"{field} no puede ser null"
                        )

                    setattr(noti, field, value)

                await self.repository.save(noti)

            return noti

        except IntegrityError as exc:
            raise UserAlreadyExistsError(
                "Error cambios "
            ) from exc

    async def delete(self, noti_id: UUID) -> None:
        async with self.session.begin():
            noti = await self.repository.find_by_id(
                noti_id
            )

            if noti is None:
                raise UserNotFoundError(
                    "Notification no encontrada"
                )

            await self.repository.delete(noti)