"""
Health-check and root endpoints.
Added to the app router so Docker / load-balancers can probe liveness.
"""
from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter()


@router.get("/health", tags=["Health"], summary="Liveness probe")
async def health():
    """Returns 200 OK with service status. Used by Docker healthcheck."""
    return {
        "status": "ok",
        "service": "praxion-backend",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/", tags=["Health"], summary="Root")
async def root():
    return {"message": "Praxion API – see /api/docs for documentation"}
