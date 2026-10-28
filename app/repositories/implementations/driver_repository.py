
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import Session, selectinload

from app.models.driver_model import Driver

from app.repositories.interfaces.driver_repository_interface import DriverRepositoryInterface

class DriverRepository(DriverRepositoryInterface):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, driver: Driver) -> Driver:
        self.db.add(driver)     #No await because it is synchrnous session-state operation.
        await self.db.flush()
        return driver

    # get driver details by id 
    async def get_by_id(self, driver_id: int):
        return await self.db.get(Driver, driver_id)      # get - retrive by primary key

    #get all driver record
    async def get_all(self):
        statement = select(Driver).order_by(Driver.id)
        result = await self.db.scalars(statement)  
        return list(result.all())

    #used selectinload to fetch drivers with their collection details as list

    async def get_with_collections(self, driver_id: int):
        statement = (
            select(Driver)
            .options(selectinload(Driver.collections))
            .where(Driver.id == driver_id)
        )
        result = await self.db.scalars(statement)
        return result.first()

    async def update(
        self, driver: Driver, changes: dict
    ) -> Driver:
        for field, value in changes.items():
            setattr(driver, field, value)

        await self.db.flush()
        return driver


    # async def delete(self, driver: Driver) -> None:
    #     await self.db.delete(driver)
    #     await self.db.flush()


    #delete through a stored procedure
    async def delete_driver_using_procedure(
        self,
        driver_id: int
    ) -> None:
        await self.db.execute(
            text("CALL delete_driver(:driver_id)"),
            {"driver_id": driver_id}
        )

        await self.db.commit()


