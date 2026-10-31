from collections.abc import AsyncGenerator

import pytest_asyncio

from httpx import ASGITransport, AsyncClient

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool

from main import app

from app.database.base import Base
from app.api.dependencies.database import get_database

# Import all models so SQLAlchemy registers their tables.
from app.models.driver_model import Driver
from app.models.transport_collection_model import TransportCollection
from app.models.user_model import User
from app.models.refresh_token_model import RefreshToken


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:

    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as db:
        try:
            yield db
        finally:
            await db.rollback()

    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:

    async def override_get_database():
        yield db_session

    app.dependency_overrides[get_database] = override_get_database

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as test_client:
        yield test_client

    app.dependency_overrides.pop(get_database, None)

    