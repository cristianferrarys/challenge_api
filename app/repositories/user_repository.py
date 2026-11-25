from abc import ABC, abstractmethod
from uuid import UUID
from app.models.user import User

class UserRepository(ABC):
    @abstractmethod
    async def find_by_id(self, user_id: UUID) -> User | None:
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    async def find_all(self) -> list[User]:
        pass

    @abstractmethod
    async def save(self, user: User) -> User:
        pass

    @abstractmethod
    async def delete(self, user: User) -> None:
        pass