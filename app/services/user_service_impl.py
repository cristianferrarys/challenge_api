from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from starlette.concurrency import run_in_threadpool

from app.core.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate,Token
from app.services.user_service import UserService

from app.auth import hash_password


class UserServiceImpl(UserService):

    def __init__(
        self,
        repository: UserRepository,
        session: AsyncSession,
    ):
        self.repository = repository
        self.session = session

    async def create(self, data: UserCreate) -> User:
        hashed_password = await run_in_threadpool(
            hash_password,
            data.password,
        )
        try:
            async with self.session.begin():
                existing = await self.repository.find_by_email(
                    data.email
                )

                if existing:
                    raise UserAlreadyExistsError(
                        "El email ya está registrado"
                    )

                user = User(
                    name=data.name,
                    email=data.email,
                    password=hashed_password
                )

                await self.repository.save(user)

            return user

        except IntegrityError as exc:
            # También protege frente a altas concurrentes.
            raise UserAlreadyExistsError(
                "El email ya está registrado"
            ) from exc

    async def get_by_id(self, user_id: UUID) -> User:
        user = await self.repository.find_by_id(user_id)

        if user is None:
            raise UserNotFoundError(
                "Usuario no encontrado"
            )

        return user

    async def get_all(self) -> list[User]:
        return await self.repository.find_all()

    async def update(
        self,
        user_id: UUID,
        data: UserUpdate,
    ) -> User:
        try:
            async with self.session.begin():
                user = await self.repository.find_by_id(
                    user_id
                )

                if user is None:
                    raise UserNotFoundError(
                        "Usuario no encontrado"
                    )

                changes = data.model_dump(
                    exclude_unset=True
                )

                for field, value in changes.items():
                    if value is None:
                        raise ValueError(
                            f"{field} no puede ser null"
                        )

                    setattr(user, field, value)

                await self.repository.save(user)

            return user

        except IntegrityError as exc:
            raise UserAlreadyExistsError(
                "El email ya está registrado"
            ) from exc

    async def delete(self, user_id: UUID) -> None:
        async with self.session.begin():
            user = await self.repository.find_by_id(
                user_id
            )

            if user is None:
                raise UserNotFoundError(
                    "Usuario no encontrado"
                )

            await self.repository.delete(user)