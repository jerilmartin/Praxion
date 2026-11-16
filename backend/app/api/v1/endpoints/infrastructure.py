"""
Infrastructure endpoints – resource discovery, inventory CRUD.   (FR-01)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

router = APIRouter()


@router.get("/", summary="List all infrastructure resources")
async def list_resources(db: AsyncSession = Depends(get_db)):
    """Return paginated list of discovered infrastructure resources."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")


@router.post("/discover", summary="Trigger infrastructure discovery")
async def trigger_discovery(db: AsyncSession = Depends(get_db)):
    """Invoke the discovery agent to scan and update the resource inventory."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")


@router.get("/{resource_id}", summary="Get a single resource")
async def get_resource(resource_id: str, db: AsyncSession = Depends(get_db)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")
