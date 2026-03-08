"""
FastAPI application factory: config, CORS, routes, middleware, error handling.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.api import health, version, network, forecast, routing, equity, anomalies, ingestion, transit
from app.schemas import ErrorDetail, ErrorResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown. Placeholder for DB pool, caches."""
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="IRIDIUM API",
        description="Real-time urban mobility prediction and optimization platform. Real data and recorded snapshots when configured; explicit status when unavailable.",
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
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health.router, tags=["health"])
    app.include_router(version.router, tags=["version"])
    app.include_router(network.router, prefix="/api/v1", tags=["network"])
    app.include_router(forecast.router, prefix="/api/v1", tags=["forecast"])
    app.include_router(routing.router, prefix="/api/v1", tags=["routing"])
    app.include_router(equity.router, prefix="/api/v1", tags=["equity"])
    app.include_router(anomalies.router, prefix="/api/v1", tags=["anomalies"])
    app.include_router(ingestion.router, prefix="/api/v1", tags=["ingestion"])
    app.include_router(transit.router, prefix="/api/v1", tags=["transit"])
    return app
