"""
Security middleware: headers and basic request size limiting.
"""

from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, *, hsts_enabled: bool, hsts_max_age_seconds: int):
        super().__init__(app)
        self._hsts_enabled = bool(hsts_enabled)
        self._hsts_max_age_seconds = int(hsts_max_age_seconds)

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)

        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        response.headers.setdefault("Cross-Origin-Resource-Policy", "same-site")
        response.headers.setdefault("Cross-Origin-Opener-Policy", "same-origin")

        # HSTS must only be enabled when the API is behind TLS.
        if self._hsts_enabled:
            response.headers.setdefault(
                "Strict-Transport-Security",
                f"max-age={self._hsts_max_age_seconds}; includeSubDomains",
            )

        return response


class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, *, max_body_bytes: int):
        super().__init__(app)
        self._max_body_bytes = int(max_body_bytes)

    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("content-length")
        if content_length:
            try:
                size = int(content_length)
            except ValueError:
                size = 0
            if size > self._max_body_bytes:
                return Response(status_code=413)
        return await call_next(request)
