"""
Dependency graph endpoints.   (FR-03, OBJ-3)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.session import get_db

router = APIRouter()


@router.get("/", summary="Return full infrastructure dependency graph")
async def get_graph(db=Depends(get_db)):
    """Return nodes and edges for frontend graph visualisation."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")


@router.get("/attack-paths", summary="Analyse potential attack paths")
async def attack_paths(db=Depends(get_db)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")
