"""
Request correlation ID middleware.
"""

from __future__ import annotations

import uuid

from app.observability.logging import get_logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class RequestIdMiddleware(BaseHTTPMiddleware):
    header_name = "X-Request-ID"

    async def dispatch(self, request: Request, call_next):
        rid = request.headers.get(self.header_name) or str(uuid.uuid4())
        request.state.request_id = rid

        response: Response = await call_next(request)
        response.headers[self.header_name] = rid
        return response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        log = get_logger("http")
        rid = getattr(request.state, "request_id", None)
        log = log.bind(request_id=rid) if rid else log

        log.info(
            "request_start",
            method=request.method,
            path=str(request.url.path),
        )
        response = await call_next(request)
        log.info(
            "request_end",
            method=request.method,
            path=str(request.url.path),
            status_code=response.status_code,
        )
        return response
