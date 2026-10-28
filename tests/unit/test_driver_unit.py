
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from datetime import date

from app.models.transport_collection_model import (
    TransportCollection,
)
from app.services.transport_collection_service import (
    TransportCollectionService,
)
from app.services.driver_service import DriverService


@pytest.mark.asyncio
async def test_get_driver_success():
    # Arrange: prepare a fake driver and repository.
    class FakeDriver:
        def __init__(self):
            self.id = 1
            self.name = "Arun"
            self.phone = "9876543210"

    driver = FakeDriver()

    repository = AsyncMock()
    repository.get_by_id.return_value = driver

    service = DriverService(
        db=AsyncMock(),
        driver_repository=repository,
    )

    # Act: call the service method.
    result = await service.get_driver(1)

    # Assert: verify the returned driver.
    assert result.id == 1
    assert result.name == "Arun"
    repository.get_by_id.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_get_driver_not_found():
    repository = AsyncMock()
    repository.get_by_id.return_value = None

    service = DriverService(
        db=AsyncMock(),
        driver_repository=repository,
    )

    with pytest.raises(HTTPException) as error:
        await service.get_driver(100)

    assert error.value.status_code == 404
    assert error.value.detail == "Driver not found"


def test_transport_collection_calculations():

    data = {
        "morning_trips": 5,
        "evening_trips": 7,
        "morning_collection": 5000,
        "evening_collection": 7000,
        "fuel_expense": 2000,
        "other_expense": 500,
    }

    service = TransportCollectionService(
        db=AsyncMock(),
        collection_repository=AsyncMock(),
    )

    # Act: execute the actual calculation function.
    result = service.calculate_totals(data)

    # Assert: verify the calculated values.
    assert result["total_trips"] == 12
    assert result["total_collection"] == 12000
    assert result["total_expense"] == 2500
    assert result["net_collection"] == 9500
