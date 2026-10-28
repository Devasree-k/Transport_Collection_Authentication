from abc import ABC, abstractmethod

from app.models.user_model import User


class UserRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    async def get_by_username(
        self,
        username: str,
    ) -> User | None:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    async def create(self, user: User) -> User:
        pass