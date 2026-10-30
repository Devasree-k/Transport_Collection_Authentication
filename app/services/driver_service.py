
from datetime import date

from fastapi import HTTPException
from sqlalchemy import and_, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.driver_model import Driver
from app.models.transport_collection_model import TransportCollection
# from repositories.driver_repository import DriverRepository
from app.repositories.interfaces.driver_repository_interface import DriverRepositoryInterface


import asyncio
import logging

from app.services.email_service import EmailService

logger = logging.getLogger(__name__)



class DriverService:

    def __init__(self, db: AsyncSession, driver_repository:DriverRepositoryInterface, email_service: EmailService):
        self.db = db
        self.driver_repository = driver_repository
        self.email_service = email_service

    async def create_driver(self, data)->Driver:
        driver = Driver(**data.model_dump())

        try:
            await self.driver_repository.create(driver)
            await self.db.commit()
            await self.db.refresh(driver)

        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=409,
                detail="Phone number already exists",
            )

        # Send admin notification after successful database commit
        email_sent = await self.email_service.send_driver_notification_async(
            driver_name=driver.name,
            phone=driver.phone,
            license_number=driver.license_number
        )

        if not email_sent:
            logger.warning("Driver registered, but admin email notification failed.")

        return driver


    async def get_drivers(self, page:int=1, limit : int=10):
        if page<1:
            raise ValueError("Page must be greater than 0")
        if limit<1 or limit>100:
            raise ValueError("Limit must be between 1 and 100")

        skip = (page - 1) * limit
        return await self.driver_repository.get_all(skip=skip, limit=limit)

    async def get_driver(self, driver_id: int):
        driver = await self.driver_repository.get_by_id(driver_id)

        if driver is None:
            raise HTTPException(
                status_code=404,
                detail="Driver not found",
            )

        return driver

    async def get_driver_with_collection(self, driver_id: int):
        driver = await self.driver_repository.get_with_collections(
            driver_id
        )

        if driver is None:
            raise HTTPException(
                status_code=404,
                detail="Driver not found",
            )

        return driver


    async def update_driver(
        self, driver_id: int, changes: dict
    ) -> Driver:
        driver = await self.get_driver(driver_id)

        try:
            await self.driver_repository.update(driver, changes)
            await self.db.commit()
            await self.db.refresh(driver)
            return driver
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=409,
                detail="Phone number or license number already exists",
            )


    async def delete_driver(self, driver_id: int) -> None:
        driver = await self.get_driver(driver_id)

        try:
            await self.driver_repository.delete_driver_using_procedure(driver_id)
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise


    #  This is for the report generation purpose 
    async def get_driver_report(
        self,
        start_date: date | None = None,
        end_date: date | None = None,
    ):
        join_conditions = [
            Driver.id == TransportCollection.driver_id
        ]

        if start_date is not None:
            join_conditions.append(
                TransportCollection.collection_date >= start_date
            )

        if end_date is not None:
            join_conditions.append(
                TransportCollection.collection_date <= end_date
            )

        statement = (
            select(
                Driver.id.label("driver_id"),
                Driver.name.label("driver_name"),
                func.count(
                    TransportCollection.id
                ).label("total_records"),
                func.coalesce(
                    func.sum(TransportCollection.total_trips), 0
                ).label("total_trips"),
                func.coalesce(
                    func.sum(TransportCollection.total_collection), 0
                ).label("total_collection"),
                func.coalesce(
                    func.sum(TransportCollection.total_expense), 0
                ).label("total_expense"),
                func.coalesce(
                    func.sum(TransportCollection.net_collection), 0
                ).label("net_collection"),
                func.max(
                    TransportCollection.total_collection
                ).label("highest_collection"),
            )
            .outerjoin(
                TransportCollection,
                and_(*join_conditions),         #unpack all the join conditions and perform left outer join 
            )
            .group_by(Driver.id, Driver.name)
            .order_by(Driver.id)
        )

        result = await self.db.execute(statement)

        return result.mappings().all()

