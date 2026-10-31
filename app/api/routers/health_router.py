
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_database

router = APIRouter(
    prefix="/health",
    tags=["Health Check"]
)


@router.get("/")
async def health_check(
    db: AsyncSession = Depends(get_database)
):

    try:
        await db.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception:
        return {
            "status": "unhealthy",
            "database": "disconnected"
        }
