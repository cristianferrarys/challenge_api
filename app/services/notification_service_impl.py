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

"""implementando estrategia """
from app.strategies.strategy_registry import (
    StrategyRegistry,
)
"""implementando estrategia """


class NotificationServiceImpl(NotificationService):

    def __init__(
        self,
        repository: NotiRepository,
        session: AsyncSession,
        registry: StrategyRegistry,
    ):
        self.repository = repository
        self.session = session
        self.registry= registry

    """metodo globar """
    async def _get_owned_notification(
            self,
            noti_id: UUID,
            user_id: UUID,
    ) -> Notification:
        noti = await self.repository.find_by_id_and_user_id(
            noti_id,
            user_id,
        )

        if noti is None:
            raise UserNotFoundError("Notificación no encontrada")
        return noti

    async def create(self, data: NotiCreate, user_id: UUID) -> Notification:

        print(data.canal)
        print(data.canal.name)
        print(data.canal.value)
        strategy = self.registry.get_strategy(data.canal.value)

        try:
            async with self.session.begin():
                notification = Notification(
                    titulo=data.titulo,
                    contenido=data.contenido,
                    canal=strategy.channel,
                    destinatario=data.destinatario,
                    user_id=user_id,
                )

                await self.repository.save(notification)
                await strategy.send(notification)
            return notification

        except IntegrityError as exc:
            # También protege frente a altas concurrentes.
            raise UserAlreadyExistsError(
                "El email ya está registrado"
            ) from exc

    async def get_by_id(self, noti_id: UUID, user_id: UUID) -> NotiResponse:
        return await self._get_owned_notification(
            noti_id,
            user_id,
        )

    async def update(
        self,
        noti_id: UUID,
        user_id: UUID,
        data: NotiUpdate,
    ) -> Notification:
        try:
            async with self.session.begin():
                noti = await self._get_owned_notification(
                    noti_id,
                    user_id,
                )
                changes = data.model_dump(exclude_unset=True)

                for field, value in changes.items():
                    if value is None:
                        raise ValueError(f"{field} no puede ser null")
                    setattr(noti, field, value)

                await self.repository.save(noti)
            return noti
        except IntegrityError as exc:
            raise UserAlreadyExistsError("Error cambios ") from exc

    async def get_my_notifications(
        self,
        user_id: UUID,
    ) -> list[Notification]:
        return await self.repository.get_by_user_id(user_id)


    async def delete(self, noti_id: UUID, user_id: UUID) -> None:
        async with self.session.begin():
            noti = await self._get_owned_notification(
                noti_id,
                user_id,
            )
            await self.repository.delete(noti)
