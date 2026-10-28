from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_database
from app.services.driver_service import DriverService

from app.api.dependencies.service_dependencies import get_driver_service

router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"],
)

@router.get("/drivers")
async def driver_report(
    start_date: date | None = None,
    end_date: date | None = None,
    service: DriverService = Depends(get_driver_service),
):
    if (
        start_date is not None
        and end_date is not None
        and start_date > end_date
    ):
        raise HTTPException(
            status_code=400,
            detail="start_date must not be after end_date",
        )

    return await service.get_driver_report(
        start_date,
        end_date,
    )
