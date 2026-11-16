"""
Security Findings endpoints.   (FR-02)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

router = APIRouter()


@router.get("/", summary="List security findings")
async def list_findings(db: AsyncSession = Depends(get_db)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")


@router.post("/scan", summary="Trigger security scan")
async def trigger_scan(db: AsyncSession = Depends(get_db)):
    """Run Checkov and Trivy against simulated infrastructure and persist results."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")


@router.get("/{finding_id}", summary="Get finding details")
async def get_finding(finding_id: str, db: AsyncSession = Depends(get_db)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")
