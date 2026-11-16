"""
Shared Pydantic schemas used across all endpoints.
"""
from __future__ import annotations
from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field

T = TypeVar("T")


class MessageResponse(BaseModel):
    """Generic success/info message response."""
    message: str
    detail: Optional[str] = None


class ErrorResponse(BaseModel):
    """Standard error envelope matching exception handlers."""
    error: str
    detail: str


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated list envelope for all list endpoints."""
    items: list[T]
    total: int
    skip: int
    limit: int
    has_more: bool = Field(default=False)

    @classmethod
    def build(cls, items: list[T], total: int, skip: int, limit: int) -> "PaginatedResponse[T]":
        return cls(
            items=items,
            total=total,
            skip=skip,
            limit=limit,
            has_more=(skip + limit) < total,
        )


class IDResponse(BaseModel):
    """Minimal response returning just a created/updated resource ID."""
    id: str


class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: str
