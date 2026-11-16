"""
Auth endpoints – login, token refresh, current user.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.security import verify_password, create_access_token

router = APIRouter()


@router.post("/login", summary="Obtain JWT access token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """Authenticate a user and return a JWT token."""
    # TODO: query user, verify password, return token
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")


@router.get("/me", summary="Current authenticated user")
async def me():
    """Return the currently authenticated user's profile."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")
