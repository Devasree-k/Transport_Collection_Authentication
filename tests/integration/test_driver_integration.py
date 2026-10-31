
from datetime import date

import pytest

from app.models.driver_model import Driver
from app.repositories.implementations.driver_repository import (
    DriverRepository,
)


@pytest.mark.asyncio
async def test_create_and_get_driver(db_session):
    # Arrange: create the repository and driver.
    repository = DriverRepository(db_session)

    driver = Driver(
        name="Arun",
        phone="9876543210",
        joined_date=date(2025, 1, 10),
        license_number="TN123456",
    )

    # Act: save and retrieve the driver.
    await repository.create(driver)
    await db_session.commit()

    result = await repository.get_by_id(driver.id)

    # Assert: check the saved database record.
    assert result is not None
    assert result.name == "Arun"
    assert result.phone == "9876543210"
    assert result.license_number == "TN123456"


@pytest.mark.asyncio
async def test_list_drivers(db_session):

    repository = DriverRepository(db_session)

    first_driver = Driver(
        name="Arun",
        phone="9876543210",
        joined_date=date(2025, 1, 10),
        license_number="TN123456",
    )

    second_driver = Driver(
        name="Priya",
        phone="9876543211",
        joined_date=date(2025, 2, 10),
        license_number="TN654321",
    )

    await repository.create(first_driver)
    await repository.create(second_driver)
    await db_session.commit()

    # Retrieve the saved drivers from the database.
    drivers = await repository.get_all()

    assert len(drivers) == 2

    driver_names = [driver.name for driver in drivers]

    assert "Arun" in driver_names
    assert "Priya" in driver_names

