
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from datetime import date

from app.models.transport_collection_model import TransportCollection
from app.services.transport_collection_service import (
    TransportCollectionService,
)
from app.services.driver_service import DriverService



@pytest.mark.asyncio
async def test_get_driver_success():

    # Arrange
    class FakeDriver:
        def __init__(self):
            self.id = 1
            self.name = "Arun"
            self.phone = "9876543210"

    driver = FakeDriver()
    repository = AsyncMock()
    repository.get_by_id.return_value = driver
    email_service = AsyncMock()

    service = DriverService(
        db=AsyncMock(),
        driver_repository=repository,
        email_service=email_service,
    )

    # Act
    result = await service.get_driver(1)

    # Assert
    assert result == driver
    repository.get_by_id.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_get_driver_success():

    # Arrange
    class FakeDriver:
        def __init__(self):
            self.id = 1
            self.name = "Arun"
            self.phone = "9876543210"

    driver = FakeDriver()
    repository = AsyncMock()
    repository.get_by_id.return_value = driver
    email_service = AsyncMock()

    service = DriverService(
        db=AsyncMock(),
        driver_repository=repository,
        email_service=email_service,
    )

    # Act
    result = await service.get_driver(1)

    # Assert
    assert result == driver
    repository.get_by_id.assert_called_once_with(1)



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

    # execute the actual calculation function.
    result = service.calculate_totals(data)

    # verify the calculated values.
    assert result["total_trips"] == 12
    assert result["total_collection"] == 12000
    assert result["total_expense"] == 2500
    assert result["net_collection"] == 9500


from app.services.transport_collection_service import (
    TransportCollectionService,
)


def test_calculate_totals():

    data = {
        "morning_trips": 10,
        "evening_trips": 15,
        "morning_collection": 5000,
        "evening_collection": 7000,
        "fuel_expense": 2000,
        "other_expense": 1000,
    }

    result = TransportCollectionService.calculate_totals(
        None, data
    )

    assert result["total_trips"] == 25
    assert result["total_collection"] == 12000
    assert result["total_expense"] == 3000
    assert result["net_collection"] == 9000


def test_calculate_totals_when_values_are_zero():

    data = {
        "morning_trips": 0,
        "evening_trips": 0,
        "morning_collection": 0,
        "evening_collection": 0,
        "fuel_expense": 0,
        "other_expense": 0,
    }

    result = TransportCollectionService.calculate_totals(
        None, data
    )

    assert result["total_trips"] == 0
    assert result["total_collection"] == 0
    assert result["total_expense"] == 0
    assert result["net_collection"] == 0
