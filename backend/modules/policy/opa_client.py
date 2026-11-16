"""
OPA Policy Client   (OBJ-4, FR-05)

Wraps HTTP calls to the Open Policy Agent sidecar.
"""
from __future__ import annotations
import httpx
from app.core.config import settings


class OPAPolicyClient:
    """Thin async client for OPA REST API."""

    def __init__(self, base_url: str = ""):
        self.base_url = base_url or settings.OPA_URL

    async def evaluate(self, policy_path: str, input_data: dict) -> bool:
        """
        Evaluate a policy rule.

        Args:
            policy_path: OPA path, e.g. "praxion/authz/allow"
            input_data: dict passed as {"input": input_data}

        Returns:
            Boolean result of the policy evaluation.
        """
        url = f"{self.base_url}/v1/data/{policy_path.lstrip('/')}"
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(url, json={"input": input_data})
            response.raise_for_status()
            return bool(response.json().get("result", False))

    async def upload_policy(self, policy_id: str, rego_content: str) -> None:
        """Upload or update a Rego policy bundle."""
        url = f"{self.base_url}/v1/policies/{policy_id}"
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.put(url, content=rego_content, headers={"Content-Type": "text/plain"})
            response.raise_for_status()
