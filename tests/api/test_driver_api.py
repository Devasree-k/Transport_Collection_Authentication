from datetime import date
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from main import app
from app.api.dependencies.auth_dependencies import get_current_user
from app.api.dependencies.service_dependencies import get_driver_service


class FakeUser:
    def __init__(self, user_id: int, role: str):
        self.id = user_id
        self.role = role
        self.is_active = True


class FakeDriver:
    def __init__(self):
        self.id = 1
        self.name = "Arun"
        self.phone = "9876543210"
        self.dob = None
        self.joined_date = date(2025, 1, 10)
        self.license_number = "TN123456"


@pytest.mark.asyncio
async def test_list_drivers_api():

    async def fake_current_user():
        return FakeUser(user_id=1, role="admin")

    mock_service = AsyncMock()
    mock_service.get_drivers.return_value = [FakeDriver()]

    app.dependency_overrides[get_current_user] = (
        fake_current_user
    )
    app.dependency_overrides[get_driver_service] = (
        lambda: mock_service
    )

    try:
        transport = ASGITransport(app=app)

        async with AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:

            response = await client.get("/api/drivers/")

        assert response.status_code == 200

        body = response.json()

        assert len(body) == 1
        assert body[0]["id"] == 1
        assert body[0]["name"] == "Arun"
        assert body[0]["phone"] == "9876543210"

        mock_service.get_drivers.assert_awaited_once()

    finally:
        # Restore the application's normal dependencies.
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_driver_forbidden_for_driver_role():

    async def fake_driver_user():
        return FakeUser(user_id=2, role="driver")

    mock_service = AsyncMock()

    app.dependency_overrides[get_current_user] = (
        fake_driver_user
    )
    app.dependency_overrides[get_driver_service] = (
        lambda: mock_service
    )

    payload = {
        "name": "Arun",
        "phone": "9876543210",
        "dob": None,
        "joined_date": "2025-01-10",
        "license_number": "TN123456",
    }

    try:
        transport = ASGITransport(app=app)

        async with AsyncClient(transport=transport, base_url="http://test",) as client:

            response = await client.post("/api/drivers/", json=payload,)

        assert response.status_code == 403

        assert response.json()["detail"] == (
            "You do not have permission to perform this action."
        )

    finally:
        app.dependency_overrides.clear()

