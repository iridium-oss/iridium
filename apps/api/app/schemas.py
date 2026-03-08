"""
Shared API response and error schemas for consistent OpenAPI and client handling.
"""

from typing import Any

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Structured error payload."""

    code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable message")
    details: dict[str, Any] | None = Field(None, description="Optional validation or context")


class ErrorResponse(BaseModel):
    """Envelope for error responses."""

    error: ErrorDetail
