"""
Agent Governance and Authorization   (OBJ-4, FR-04, FR-05)

Responsibilities:
- Manage agent identities and permission sets
- Evaluate agent operations against OPA policies before execution
- Record authorization decisions
"""
from __future__ import annotations
import httpx
from app.core.config import settings


class GovernanceAgent:
    """Manages agent identities and enforces policy-based authorization."""

    def __init__(self, db_session=None):
        self.db = db_session
        self.opa_url = settings.OPA_URL

    async def register_agent(self, name: str, role: str, permissions: dict) -> dict:
        """Create a new agent identity record."""
        # TODO: insert Agent record, return agent dict
        raise NotImplementedError

    async def authorize(self, agent_id: str, operation: str, resource: str) -> bool:
        """
        Evaluate whether agent_id may perform operation on resource.
        Sends a query to OPA and records the decision.

        Returns True if allowed, False if denied.
        """
        input_data = {
            "agent_id": agent_id,
            "operation": operation,
            "resource": resource,
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.opa_url}/v1/data/praxion/authz/allow",
                    json={"input": input_data},
                )
                result = response.json()
                return bool(result.get("result", False))
        except Exception:
            # Fail closed – deny on error
            return False

    async def update_permissions(self, agent_id: str, permissions: dict) -> dict:
        """Update an agent's allowed operations."""
        raise NotImplementedError
