"""
Human approval workflow endpoints.   (FR-08, OBJ-7)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.session import get_db

router = APIRouter()


@router.get("/", summary="List approval requests")
async def list_approvals(db=Depends(get_db)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")


@router.post("/{approval_id}/approve", summary="Approve a pending operation")
async def approve(approval_id: str, db=Depends(get_db)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")


@router.post("/{approval_id}/reject", summary="Reject a pending operation")
async def reject(approval_id: str, db=Depends(get_db)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")
