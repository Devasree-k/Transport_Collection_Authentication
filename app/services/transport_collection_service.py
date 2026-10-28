from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transport_collection_model import TransportCollection
from app.repositories.implementations.transport_collection_repository import (
    TransportCollectionRepository,
)

from app.repositories.interfaces.transport_collection_repository_interface import TransportCollectionRepositoryInterface

class TransportCollectionService:

    def __init__(self, db: AsyncSession, collection_repository :TransportCollectionRepositoryInterface):
        self.db = db
        self.repository = collection_repository


    #  Calculate totals 
    def calculate_totals(self, data: dict) -> dict:
        total_trips = (
            data["morning_trips"] + data["evening_trips"]
        )

        total_collection = (
            data["morning_collection"] + data["evening_collection"]
        )

        total_expense = (
            data["fuel_expense"] + data["other_expense"]
        )

        return {
            "total_trips": total_trips,
            "total_collection": total_collection,
            "total_expense": total_expense,
            "net_collection": total_collection - total_expense,
        }

    # Read collection by id
    async def get_collection(self, collection_id: int):
        collection = await self.repository.get_by_id(collection_id)

        if collection is None:
            raise HTTPException(
                status_code=404,
                detail="Collection not found",
            )

        return collection

#create a collection 
    async def create_collection(self, data):
        values = data.model_dump()

        driver = await self.repository.get_driver(
            values["driver_id"]
        )

        if driver is None:
            raise HTTPException(
                status_code=404,
                detail="Driver id not found",
            )

        values.update(self.calculate_totals(values))

        collection = TransportCollection(**values)

        try:
            await self.repository.create(collection)
            await self.db.commit()

            return await self.get_collection(collection.id)

        except Exception:
            await self.db.rollback()
            raise

    # to retrive all the collections
    async def get_collections(self):
        return await self.repository.get_all()

    async def update_collection(
        self,
        collection_id: int,
        changes: dict,
    ):
        collection = await self.get_collection(collection_id)

        values = {
            "driver_id": collection.driver_id,
            "vehicle_number": collection.vehicle_number,
            "collection_date": collection.collection_date,
            "morning_trips": collection.morning_trips,
            "evening_trips": collection.evening_trips,
            "morning_collection": collection.morning_collection,
            "evening_collection": collection.evening_collection,
            "fuel_expense": collection.fuel_expense,
            "other_expense": collection.other_expense,
        }

        values.update(changes)

        driver = await self.repository.get_driver(
            values["driver_id"]
        )

        if driver is None:
            raise HTTPException(
                status_code=404,
                detail="Driver not found",
            )

        calculated = self.calculate_totals(values)

        try:
            for field, value in changes.items():
                setattr(collection, field, value)

            for field, value in calculated.items():
                setattr(collection, field, value)

            await self.db.commit()

            return await self.get_collection(collection_id)

        except Exception:
            await self.db.rollback()
            raise


    # delete collection 
    async def delete_collection(self, collection_id: int):
        collection = await self.get_collection(collection_id)

        try:
            await self.repository.delete(collection)
            await self.db.commit()

            return {"message": "Collection deleted"}

        except Exception:
            await self.db.rollback()
            raise
