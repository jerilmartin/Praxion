"""
Remediation Planning and Execution Agent   (OBJ-7, FR-08)

Responsibilities:
- Use LLM to propose remediation actions for security findings
- Route sensitive actions through human approval workflow
- Execute approved remediations in a controlled, auditable manner
- Verify post-remediation state
"""
from __future__ import annotations
from typing import Any


class RemediationPlannerAgent:
    """Generates remediation proposals using an LLM."""

    def __init__(self, llm=None, db_session=None):
        self.llm = llm
        self.db = db_session

    async def propose(self, finding: dict) -> dict:
        """
        Given a SecurityFinding, generate a human-readable remediation plan.

        Returns:
            dict with keys: proposed_action, risk_level, requires_approval
        """
        # TODO: build prompt, call LLM, parse structured response
        raise NotImplementedError


class RemediationExecutorAgent:
    """Executes approved remediations and verifies results."""

    def __init__(self, db_session=None):
        self.db = db_session

    async def execute(self, remediation_id: str) -> dict[str, Any]:
        """Execute a previously approved remediation record."""
        # TODO: load RemediationRecord, apply change to simulated infra, record result
        raise NotImplementedError

    async def verify(self, remediation_id: str) -> dict[str, Any]:
        """Re-scan the affected resource to confirm the fix was applied."""
        raise NotImplementedError
