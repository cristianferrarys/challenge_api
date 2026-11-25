from starlette.concurrency import run_in_threadpool

from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    verify_access_token,
)

from app.core.exceptions import (
    InvalidCredentialsError,
    InvalidAccessTokenError,
)

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import Token
from app.services.auth_service import AuthService


DUMMY_HASH = hash_password("dummy-password-not-for-login")


class AuthServiceImpl(AuthService):

    def __init__(
        self,
        repository: UserRepository,
    ):
        self.repository = repository

    async def login(
        self,
        email: str,
        password: str,
    ) -> Token:

        user = await self.repository.find_by_email(email)

        stored_hash = user.password if user else DUMMY_HASH

        valid = await run_in_threadpool(
            verify_password,
            password,
            stored_hash,
        )

        if user is None or not valid:
            raise InvalidCredentialsError(
                "Credenciales inválidas"
            )

        access_token = create_access_token(
            data={"sub": str(user.id)}
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
        )

    async def get_current_user(
        self,
        token: str,
    ) -> User:

        user_id = verify_access_token(token)

        if user_id is None:
            raise InvalidAccessTokenError(
                "Token inválido o expirado"
            )

        user = await self.repository.find_by_id(user_id)

        if user is None:
            raise InvalidAccessTokenError(
                "Usuario no disponible"
            )

        return user