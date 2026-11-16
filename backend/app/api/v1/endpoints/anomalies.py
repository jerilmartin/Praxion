"""
Anomaly detection endpoints.   (FR-07, OBJ-5)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.session import get_db

router = APIRouter()


@router.get("/", summary="List anomaly records")
async def list_anomalies(db=Depends(get_db)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")


@router.post("/analyse/{agent_id}", summary="Run anomaly analysis for an agent")
async def analyse_agent(agent_id: str, db=Depends(get_db)):
    """Trigger Isolation Forest scoring for the specified agent's recent activity."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")
