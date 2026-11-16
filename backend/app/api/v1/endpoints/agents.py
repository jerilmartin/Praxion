"""
Agent management endpoints.   (FR-04)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

router = APIRouter()


@router.get("/", summary="List registered agents")
async def list_agents(db: AsyncSession = Depends(get_db)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")


@router.post("/", summary="Register a new agent")
async def register_agent(db: AsyncSession = Depends(get_db)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")


@router.get("/{agent_id}", summary="Get agent details")
async def get_agent(agent_id: str, db: AsyncSession = Depends(get_db)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")


@router.patch("/{agent_id}/permissions", summary="Update agent permissions")
async def update_permissions(agent_id: str, db: AsyncSession = Depends(get_db)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")
