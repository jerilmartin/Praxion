"""
Remediation endpoints.   (FR-08, OBJ-7)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.session import get_db

router = APIRouter()


@router.get("/", summary="List remediation records")
async def list_remediations(db=Depends(get_db)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")


@router.post("/propose/{finding_id}", summary="Propose remediation for a finding")
async def propose_remediation(finding_id: str, db=Depends(get_db)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")


@router.post("/{remediation_id}/execute", summary="Execute an approved remediation")
async def execute_remediation(remediation_id: str, db=Depends(get_db)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")
