
import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from app.api.routers.auth_router import router as auth_router
from app.api.routers.driver_router import router as driver_router
from app.api.routers.transport_collection_router import (
    router as collection_router,
)
from app.api.routers.report_router import router as report_router

from app.core.logging_config import configure_logging
from app.database.connection import engine
from app.middleware.observability import RequestLoggingMiddleware


# Configure logging
configure_logging()

# Create the logger
logger = logging.getLogger(__name__)


# Application startup and shutdown
@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:

    logger.info("Transport Collection API starting")

    try:
        yield

    finally:
        logger.info("Transport Collection API shutting down")
        await engine.dispose()


#  Create the FastAPI application
app = FastAPI(
    title="Transport Collection System",
    description=(
        "Transport collection management with async SQLAlchemy, "
        "JWT authentication, and role-based authorization."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


# Register middleware
app.add_middleware(RequestLoggingMiddleware)


# Register routers
app.include_router(auth_router)
app.include_router(driver_router)
app.include_router(collection_router)
app.include_router(report_router)


# Home endpoint
@app.get("/")
async def home() -> dict[str, str]:
    return {
        "message": "Transport Collection System"
    }

