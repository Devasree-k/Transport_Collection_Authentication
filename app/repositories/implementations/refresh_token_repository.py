import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token_model import RefreshToken

from app.repositories.interfaces.refresh_token_repository_interface import (
    RefreshTokenRepositoryInterface,
)

from app.exceptions.custom_exception import (
    RepositoryError,
    RegistrationConflict
)


logger = logging.getLogger(__name__)


class RefreshTokenRepository(RefreshTokenRepositoryInterface):

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    # Create refresh token
    async def create( self, token: RefreshToken) -> RefreshToken:
        try:
            self.db.add(token)
            await self.db.flush()
            return token

        except IntegrityError as exc:
            logger.exception("Refresh token creation conflict")
            raise RegistrationConflict("Refresh token already exists") from exc

        except SQLAlchemyError as exc:
            logger.exception("Error creating refresh token")
            raise RepositoryError("Unable to create refresh token") from exc



    # Get refresh token using its hash
    async def get_by_hash( self, token_hash: str) -> RefreshToken | None:
        try:
            statement = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
            return await self.db.scalar(statement)

        except SQLAlchemyError as exc:
            logger.exception("Error retrieving refresh token")
            raise RepositoryError("Unable to retrieve refresh token") from exc

