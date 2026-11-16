"""
Agent security simulation endpoints.   (FR-06, OBJ-5)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.session import get_db

router = APIRouter()


@router.get("/scenarios", summary="List available simulation scenarios")
async def list_scenarios():
    return {
        "scenarios": [
            "unauthorized_tool_access",
            "privilege_escalation",
            "prompt_injection",
            "agent_communication_abuse",
        ]
    }


@router.post("/run/{scenario}", summary="Run a specific attack simulation")
async def run_simulation(scenario: str, db=Depends(get_db)):
    """Execute the named simulation and record whether Praxion detected/blocked it."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented yet")
