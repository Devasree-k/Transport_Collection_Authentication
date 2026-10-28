# python -m pip install pytest pytest-asyncio httpx aiosqlite


from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool

from app.database.base import Base
from app.models.driver_model import Driver
from app.models.transport_collection_model import TransportCollection


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    # Create fresh tables for each test.
    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all) 

    async with TestingSessionLocal() as db:
        try:
            yield db
        finally:
            await db.rollback()

    # Remove tables after the test finishes.
    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)

        