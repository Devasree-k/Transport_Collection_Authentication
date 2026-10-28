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

