"""
Custom exception classes and FastAPI exception handlers.
Register handlers in application.py so all errors return consistent JSON.
"""
from __future__ import annotations
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


# ── Custom exception types ────────────────────────────────────────────────────

class PraxionError(Exception):
    """Base exception for all Praxion domain errors."""
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "An unexpected error occurred"

    def __init__(self, detail: str | None = None):
        self.detail = detail or self.__class__.detail


class NotFoundError(PraxionError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Resource not found"


class UnauthorizedError(PraxionError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Authentication required"


class ForbiddenError(PraxionError):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Operation not permitted by policy"


class PolicyViolationError(ForbiddenError):
    """Raised when OPA denies an agent operation."""
    detail = "Agent operation denied by authorization policy"


class ConflictError(PraxionError):
    status_code = status.HTTP_409_CONFLICT
    detail = "Resource already exists"


class ValidationError(PraxionError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Validation error"


# ── Handler registration ──────────────────────────────────────────────────────

def register_exception_handlers(app: FastAPI) -> None:
    """Call this inside create_app() to wire up all handlers."""

    @app.exception_handler(PraxionError)
    async def praxion_error_handler(request: Request, exc: PraxionError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.__class__.__name__, "detail": exc.detail},
        )

    @app.exception_handler(Exception)
    async def generic_error_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "InternalServerError", "detail": str(exc)},
        )
