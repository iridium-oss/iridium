"""
FastAPI application factory: config, CORS, routes, middleware, error handling.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.config import get_settings
from app.api import (
    health,
    version,
    network,
    forecast,
    routing,
    equity,
    anomalies,
    ingestion,
    transit,
    system,
    weather,
    digital_twin,
    alerts,
    federated,
    eo,
)
from app.schemas import ErrorDetail, ErrorResponse
from app.observability.logging import configure_logging
from app.middleware.request_id import RequestIdMiddleware, RequestLoggingMiddleware
from app.middleware.security import RequestSizeLimitMiddleware, SecurityHeadersMiddleware


def _propagate_provider_env(settings) -> None:
    """Propagate IRIDIUM_* and legacy credentials into os.environ for adapters that read env directly."""
    import os
    if settings.twogis.api_key and not os.environ.get("TWOGIS_API_KEY"):
        os.environ["TWOGIS_API_KEY"] = settings.twogis.api_key.get_secret_value()
    if settings.twogis.api_key and not os.environ.get("IRIDIUM_TWOGIS__API_KEY"):
        os.environ["IRIDIUM_TWOGIS__API_KEY"] = settings.twogis.api_key.get_secret_value()
    if settings.moovit.api_key:
        if not os.environ.get("MOOVIT_PARTNER_API_KEY"):
            os.environ["MOOVIT_PARTNER_API_KEY"] = settings.moovit.api_key.get_secret_value()
        if not os.environ.get("MOOVIT_API_KEY"):
            os.environ["MOOVIT_API_KEY"] = settings.moovit.api_key.get_secret_value()
    if settings.moovit.base_url and not os.environ.get("MOOVIT_PARTNER_BASE_URL"):
        os.environ["MOOVIT_PARTNER_BASE_URL"] = settings.moovit.base_url
    if settings.gomap.api_key and not os.environ.get("GOMAP_API_KEY"):
        os.environ["GOMAP_API_KEY"] = settings.gomap.api_key.get_secret_value()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown. Placeholder for DB pool, caches."""
    settings = get_settings()
    configure_logging(settings.LOG_LEVEL)
    _propagate_provider_env(settings)
    # Trigger optional engine creation early for fail-fast behavior when enabled
    from app.db.engine import get_engine

    get_engine()
    yield  # pragma: no cover


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="IRIDIUM API",
        description=(
            "Urban mobility prediction and optimization platform. "
            "Real data and recorded snapshots when configured, explicit status when unavailable."
        ),
        version=settings.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
        responses={
            400: {"model": ErrorResponse, "description": "Validation or bad request"},
            404: {"model": ErrorResponse, "description": "Resource not found"},
            500: {"model": ErrorResponse, "description": "Internal server error"},
        },
    )

    @app.exception_handler(ValueError)
    def handle_value_error(request: Request, exc: ValueError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"error": {"code": "invalid_value", "message": str(exc), "details": None}},
        )

    @app.exception_handler(RequestValidationError)
    def handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
        sanitized = []
        for e in exc.errors():
            sanitized.append(
                {
                    "loc": e.get("loc"),
                    "msg": e.get("msg"),
                    "type": e.get("type"),
                }
            )
        err = ErrorResponse(
            error=ErrorDetail(
                code="validation_error",
                message="Request validation failed",
                details={"errors": sanitized},
            )
        )
        return JSONResponse(status_code=400, content=err.model_dump(mode="json"))

    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(
        RequestSizeLimitMiddleware,
        max_body_bytes=settings.core.max_request_body_bytes,
    )
    app.add_middleware(
        SecurityHeadersMiddleware,
        hsts_enabled=settings.core.hsts_enabled,
        hsts_max_age_seconds=settings.core.hsts_max_age_seconds,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list(),
        allow_credentials=settings.core.cors_allow_credentials,
        allow_methods=settings.core.cors_allow_methods_list(),
        allow_headers=settings.core.cors_allow_headers_list(),
    )
    app.include_router(health.router, tags=["health"])
    app.include_router(version.router, tags=["version"])
    app.include_router(system.router, prefix="/api/v1", tags=["system"])
    app.include_router(alerts.router, prefix="/api/v1", tags=["alerts"])
    app.include_router(weather.router, prefix="/api/v1", tags=["weather"])
    app.include_router(digital_twin.router, prefix="/api/v1", tags=["digital-twin"])
    app.include_router(network.router, prefix="/api/v1", tags=["network"])
    app.include_router(forecast.router, prefix="/api/v1", tags=["forecast"])
    app.include_router(routing.router, prefix="/api/v1", tags=["routing"])
    app.include_router(equity.router, prefix="/api/v1", tags=["equity"])
    app.include_router(anomalies.router, prefix="/api/v1", tags=["anomalies"])
    app.include_router(ingestion.router, prefix="/api/v1", tags=["ingestion"])
    app.include_router(transit.router, prefix="/api/v1", tags=["transit"])
    app.include_router(federated.router, prefix="/api/v1", tags=["federated"])
    app.include_router(eo.router, prefix="/api/v1", tags=["earth-observation"])
    return app
