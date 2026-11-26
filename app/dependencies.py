from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.user_repository_impl import UserRepositoryImpl
from app.services.user_service import UserService
from app.services.user_service_impl import UserServiceImpl
"""auth"""
from fastapi.security import OAuth2PasswordBearer
from app.services.auth_service import AuthService
from app.services.auth_service_impl import AuthServiceImpl
from app.core.database import SessionLocal
from app.models.user import User
"""auth"""

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





def get_auth_service(
    repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
) -> AuthService:

    return AuthServiceImpl(
        repository=repository
    )

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="auth/token"
)
async def get_current_user(
    token: Annotated[
        str,
        Depends(oauth2_schema),
    ],
) -> User:

    async with SessionLocal() as session:

        repository = UserRepositoryImpl(session)

        service = AuthServiceImpl(repository)

        return await service.get_current_user(token)

