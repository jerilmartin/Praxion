"""
Reusable FastAPI dependencies.
Import from here rather than duplicating boilerplate across endpoints.
"""
from __future__ import annotations
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import decode_access_token
from app.db.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# ── Database session ──────────────────────────────────────────────────────────

DBSession = Annotated[AsyncSession, Depends(get_db)]

# ── Pagination ────────────────────────────────────────────────────────────────


class PaginationParams:
    def __init__(
        self,
        skip: int = Query(default=0, ge=0, description="Number of records to skip"),
        limit: int = Query(default=50, ge=1, le=500, description="Max records to return"),
    ):
        self.skip = skip
        self.limit = limit


Pagination = Annotated[PaginationParams, Depends(PaginationParams)]

# ── Current user ──────────────────────────────────────────────────────────────


async def get_current_user_id(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    """Decode JWT and return the user ID (subject). Raises 401 on failure."""
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id: Optional[str] = payload.get("sub")
        if user_id is None:
            raise credentials_exc
        return user_id
    except JWTError:
        raise credentials_exc


CurrentUserId = Annotated[str, Depends(get_current_user_id)]
