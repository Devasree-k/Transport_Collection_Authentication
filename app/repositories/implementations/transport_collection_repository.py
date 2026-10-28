
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import joinedload

from app.models.driver_model import Driver
from app.models.transport_collection_model import TransportCollection

from app.repositories.interfaces.transport_collection_repository_interface import TransportCollectionRepositoryInterface

class TransportCollectionRepository(TransportCollectionRepositoryInterface):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_driver(self, driver_id: int):
        return await self.db.get(Driver, driver_id)


    async def create(self, collection: TransportCollection):
        self.db.add(collection)
        await self.db.flush()
        return collection


    async def get_by_id(self, collection_id: int):
        statement = (
            select(TransportCollection)
            .options(joinedload(TransportCollection.driver))
            .where(TransportCollection.id == collection_id)
        )
        result = await self.db.scalars(statement)

        return result.unique().first()


    async def get_all(self):
        statement = (
            select(TransportCollection)
            .options(joinedload(TransportCollection.driver))
            .order_by(TransportCollection.id)
        )
        # return await list(self.db.scalars(statement).unique().all())
        result = await self.db.scalars(statement)

        return list(result.unique().all())

    async def update_collection(
        self,
        collection: TransportCollection,
        update_data: dict,
    ) -> TransportCollection:
        for field, value in update_data.items():
            setattr(collection, field, value)

        await self.db.flush()
        return collection


    async def delete(self, collection: TransportCollection) -> None:
        await self.db.delete(collection)
        await self.db.flush()

