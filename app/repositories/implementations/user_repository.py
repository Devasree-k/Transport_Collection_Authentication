import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import User

from app.repositories.interfaces.user_repository_interface import (
    UserRepositoryInterface,
)

from app.exceptions.custom_exception import (
    RepositoryError,
    RegistrationConflict,
)


logger = logging.getLogger(__name__)


class UserRepository(UserRepositoryInterface):

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    # Get user by ID
    async def get_by_id( self, user_id: int ) -> User | None:
        try:
            return await self.db.get(User, user_id)

        except SQLAlchemyError as exc:
            logger.exception("Error retrieving user ID %s",user_id)
            raise RepositoryError("Unable to retrieve user") from exc



    # Get user by username
    async def get_by_username(self,username: str ) -> User | None:
        try:
            username = username.strip().lower()
            statement = select(User).where(
                User.username == username
            )

            return await self.db.scalar(statement)

        except SQLAlchemyError as exc:
            logger.exception("Error retrieving user by username")
            raise RepositoryError("Unable to retrieve user") from exc

    # Get user by email
    async def get_by_email(self, email: str) -> User | None:

        try:
            email = email.strip().lower()
            statement = select(User).where(
                User.email == email
            )

            return await self.db.scalar(statement)

        except SQLAlchemyError as exc:
            logger.exception("Error retrieving user by email" )

            raise RepositoryError("Unable to retrieve user") from exc

    # Create user
    async def create(self, user: User) -> User:
        try:
            self.db.add(user)
            await self.db.flush()

            return user

        except IntegrityError as exc:
            logger.exception("Username or email already exists" )
            raise RegistrationConflict("Username or email already exists" ) from exc

        except SQLAlchemyError as exc:
            logger.exception("Error creating user")
            raise RepositoryError("Unable to create user" ) from exc

