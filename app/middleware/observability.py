
import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

logger = logging.getLogger("app.requests")


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request,call_next: RequestResponseEndpoint) -> Response:

        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        start_time = time.perf_counter()

        try:
            response = await call_next(request)

        except Exception:
            duration = (time.perf_counter() - start_time) * 1000

            logger.exception(
                "request_id=%s %s %s failed after %.2fms",
                request_id,
                request.method,
                request.url.path,
                duration
            )

            response = JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"}
            )

        duration = (time.perf_counter() - start_time) * 1000

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time-ms"] = f"{duration:.2f}"

        logger.info(
            "request_id=%s %s %s status=%s duration_ms=%.2f",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration
        )

        return response
