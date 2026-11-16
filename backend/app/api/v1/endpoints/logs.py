"""
Activity log endpoints.   (FR-09, OBJ-6)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.session import get_db

router = APIRouter()


@router.get("/", summary="List agent activity logs")
async def list_logs(db=Depends(get_db)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")


@router.get("/agent/{agent_id}", summary="Logs for a specific agent")
async def logs_for_agent(agent_id: str, db=Depends(get_db)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")
