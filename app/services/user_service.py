from abc import ABC, abstractmethod
from uuid import UUID
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class UserService(ABC):
    @abstractmethod
    async def create(self, data: UserCreate) -> User:
        pass
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User:
        pass
    @abstractmethod
    async def get_all(self) -> list[User]:
        pass

    @abstractmethod
    async def update(
        self,
        user_id: UUID,
        data: UserUpdate,
    ) -> User:
        pass

    @abstractmethod
    async def delete(self, user_id: UUID) -> None:
        pass