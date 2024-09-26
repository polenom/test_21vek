import logging
from fastapi import Request, Response, HTTPException

from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggingBadRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: callable) -> Response:
        response: Response = await call_next(request)
        if response.status_code >= 400:
            logger.error(f"Bad request: {request.method} {request.url}")

        return response
