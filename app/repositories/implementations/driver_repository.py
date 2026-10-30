

import logging

from sqlalchemy import select, text

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.driver_model import Driver

from app.repositories.interfaces.driver_repository_interface import (
    DriverRepositoryInterface,
)

from app.exceptions.custom_exception import (
    RepositoryError,
    RegistrationConflict
)


logger = logging.getLogger(__name__)


class DriverRepository(DriverRepositoryInterface):

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    # Create driver
    async def create(self, driver: Driver) -> Driver:
        try:
            self.db.add(driver)
            await self.db.flush()

            return driver

        except IntegrityError:
            logger.exception("Driver creation conflict")
            raise RegistrationConflict("Driver details already exist" )

        except SQLAlchemyError:
            logger.exception("Error creating driver")
            raise RepositoryError("Unable to create driver")

    # Get driver by ID
    async def get_by_id(self, driver_id: int ) -> Driver | None:

        try:
            return await self.db.get(Driver, driver_id)

        except SQLAlchemyError as exc:
            logger.exception(
                "Error retrieving driver with ID %s",
                driver_id
            )
            raise RepositoryError("Unable to retrieve driver") from exc

    # Get all drivers with pagination
    async def get_all(self, skip: int = 0, limit: int = 10 ) -> list[Driver]:

        try:
            statement = (
                select(Driver)
                .order_by(Driver.id)
                .offset(skip)
                .limit(limit)
            )

            result = await self.db.scalars(statement)
            return list(result.all())

        except SQLAlchemyError as exc:
            logger.exception("Error retrieving all drivers")
            raise RepositoryError("Unable to retrieve drivers") from exc

    # Get driver with collections
    async def get_with_collections( self, driver_id: int) -> Driver | None:

        try:
            statement = (
                select(Driver)
                .options(selectinload(Driver.collections))
                .where(Driver.id == driver_id)
            )

            result = await self.db.scalars(statement)
            return result.first()

        except SQLAlchemyError:
            logger.exception(
                "Error retrieving driver collections for ID %s",
                driver_id
            )
            raise RepositoryError("Unable to retrieve driver collections")

    # Update driver
    async def update(self, driver: Driver, changes: dict[str, object]) -> Driver:

        try:
            for field, value in changes.items():
                setattr(driver, field, value)

            await self.db.flush()
            return driver

        except IntegrityError as exc:
            logger.exception("Driver update conflict")
            raise RegistrationConflict("Driver details already exist") from exc

        except SQLAlchemyError as exc:
            logger.exception("Error updating driver")
            raise RepositoryError("Unable to update driver") from exc

    # Delete driver through stored procedure
    async def delete_driver_using_procedure( self, driver_id: int) -> None:

        try:
            await self.db.execute(
                text("CALL delete_driver(:driver_id)"),
                {"driver_id": driver_id}
            )

            await self.db.flush()

        except SQLAlchemyError as exc:
            logger.exception("Error deleting driver with ID %s",driver_id )
            raise RepositoryError("Unable to delete driver") from exc
