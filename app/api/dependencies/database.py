from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import SessionLocal


async def get_database() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        yield db
