from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import User
from app.repositories.interfaces.user_repository_interface import (
    UserRepositoryInterface,
)


class UserRepository(UserRepositoryInterface):

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.db.get(User, user_id)

    async def get_by_username(
        self,
        username: str,
    ) -> User | None:
        statement = select(User).where(
            User.username == username
        )
        return await self.db.scalar(statement)

    async def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return await self.db.scalar(statement)

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush()
        return user