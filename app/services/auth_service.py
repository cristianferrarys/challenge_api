from abc import ABC, abstractmethod

from app.models.user import User
from app.schemas.user import Token


class AuthService(ABC):
    @abstractmethod
    async def login(
        self,
        email: str,
        password: str,
    ) -> Token:
        pass

    @abstractmethod
    async def get_current_user(
        self,
        token: str,
    ) -> User:
        pass