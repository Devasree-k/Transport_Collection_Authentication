import pytest
from sqlalchemy import select
from app.api.dependencies.database import get_database
from app.models.user_model import User
from app.core.security import hash_refresh_token
from app.models.refresh_token_model import RefreshToken

@pytest.mark.asyncio
async def test_duplicate_registration_returns_conflict(client):
    payload = {"username": "testdriver", 
               "email": "driver@example.com", 
               "password": "StrongPassword123!"
               }
    assert (await client.post("/api/auth/register", json=payload)).status_code == 201
    duplicate = await client.post("/api/auth/register", json=payload)
    assert duplicate.status_code == 409

@pytest.mark.asyncio
async def test_me_requires_access_token(client):
    response = await client.get("/api/auth/me")
    assert response.status_code == 401
