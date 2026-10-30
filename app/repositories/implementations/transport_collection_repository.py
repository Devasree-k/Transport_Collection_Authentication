import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.driver_model import Driver
from app.models.transport_collection_model import TransportCollection

from app.repositories.interfaces.transport_collection_repository_interface import (
    TransportCollectionRepositoryInterface,
)

from app.exceptions.custom_exception import (
    RepositoryError,
    RegistrationConflict
)


logger = logging.getLogger(__name__)


class TransportCollectionRepository(
    TransportCollectionRepositoryInterface
):

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    # Get driver by ID
    async def get_driver( self, driver_id: int) -> Driver | None:
        try:
            return await self.db.get(Driver, driver_id)

        except SQLAlchemyError as exc:
            logger.exception("Error retrieving driver ID %s", driver_id)
            raise RepositoryError("Unable to retrieve driver") from exc


    # Create transport collection
    async def create( self, collection: TransportCollection) -> TransportCollection:
        try:
            self.db.add(collection)
            await self.db.flush()
            return collection

        except IntegrityError as exc:
            logger.exception("Collection creation conflict")
            raise RegistrationConflict("Collection details violate a database constraint" ) from exc

        except SQLAlchemyError as exc:
            logger.exception("Error creating collection")
            raise RepositoryError("Unable to create collection") from exc



    # Get collection by ID
    async def get_by_id( self, collection_id: int ) -> TransportCollection | None:
        try:
            statement = (
                select(TransportCollection)
                .options(
                    joinedload(TransportCollection.driver)
                )
                .where(
                    TransportCollection.id == collection_id
                )
            )

            result = await self.db.scalars(statement)
            return result.unique().first()

        except SQLAlchemyError as exc:
            logger.exception("Error retrieving collection ID %s", collection_id )
            raise RepositoryError( "Unable to retrieve collection") from exc

    # Get all collections with pagination
    async def get_all(self, skip: int = 0, limit: int = 10 ) -> list[TransportCollection]:
        try:
            statement = (
                select(TransportCollection)
                .options(
                    joinedload(TransportCollection.driver)
                )
                .order_by(TransportCollection.id)
                .offset(skip)
                .limit(limit)
            )

            result = await self.db.scalars(statement)
            return list(result.unique().all())

        except SQLAlchemyError as exc:
            logger.exception("Error retrieving all transport collections")
            raise RepositoryError("Unable to retrieve collections") from exc

    # Update collection
    async def update_collection( self, 
                                collection: TransportCollection, 
                                update_data: dict[str, object]
                                ) -> TransportCollection:

        try:
            for field, value in update_data.items():
                setattr(collection, field, value)
            await self.db.flush()
            return collection

        except IntegrityError as exc:
            logger.exception("Collection update conflict")
            raise RegistrationConflict("Collection details violate a database constraint") from exc

        except SQLAlchemyError as exc:
            logger.exception("Error updating collection")
            raise RepositoryError("Unable to update collection" ) from exc



    # Delete collection
    async def delete( self, collection: TransportCollection) -> None:
        try:
            await self.db.delete(collection)
            await self.db.flush()

        except SQLAlchemyError as exc:
            logger.exception( "Error deleting collection ID %s", collection.id)
            raise RepositoryError("Unable to delete collection") from exc

