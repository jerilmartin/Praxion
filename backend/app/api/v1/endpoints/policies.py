"""
Policy management endpoints.   (FR-05, OBJ-4)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.session import get_db

router = APIRouter()


@router.get("/", summary="List OPA policies")
async def list_policies(db=Depends(get_db)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")


@router.post("/evaluate", summary="Evaluate an operation against active policies")
async def evaluate_policy(db=Depends(get_db)):
    """Submit an agent operation for OPA policy evaluation."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")
