from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.user_repository_impl import UserRepositoryImpl
from app.services.user_service import UserService
from app.services.user_service_impl import UserServiceImpl


def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> UserRepository:
    return UserRepositoryImpl(session)


def get_user_service(
    repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
    session: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
) -> UserService:
    return UserServiceImpl(
        repository=repository,
        session=session,
    )