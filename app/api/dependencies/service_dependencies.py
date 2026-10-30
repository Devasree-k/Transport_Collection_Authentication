from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_database

from app.repositories.implementations.driver_repository import DriverRepository
from app.repositories.implementations.transport_collection_repository import TransportCollectionRepository
from app.repositories.implementations.user_repository import UserRepository
from app.repositories.implementations.refresh_token_repository import RefreshTokenRepository

from app.services.driver_service import DriverService
from app.services.transport_collection_service import TransportCollectionService
from app.services.auth_service import AuthService

from app.services.email_service import EmailService


def get_driver_service(db: AsyncSession = Depends(get_database)) -> DriverService:
    # return DriverService(db, DriverRepository(db))
    driver_repository = DriverRepository(db)
    email_service = EmailService()

    return DriverService(
        db,
        driver_repository,
        email_service
    )


def get_collection_service(db: AsyncSession = Depends(get_database)) -> TransportCollectionService:
    return TransportCollectionService(db, 
                                    TransportCollectionRepository(db)
                                    )

def get_auth_service(db: AsyncSession = Depends(get_database)) -> AuthService:
    return AuthService(db, 
                       UserRepository(db), 
                       RefreshTokenRepository(db)
                       )
