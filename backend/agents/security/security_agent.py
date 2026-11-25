"""
Security Analysis Agent   (OBJ-2, FR-02)

Responsibilities:
- Run Checkov against Terraform configurations
- Run Trivy against container images / IaC manifests
- Parse scan results and persist SecurityFinding records
- Assign initial severity and risk scores
"""
from __future__ import annotations
import subprocess
import json
from pathlib import Path

from agents.base_agent import BaseAgent


class SecurityScanAgent(BaseAgent):
    """Wraps Checkov and Trivy CLI tools to produce SecurityFinding records."""

    agent_role = "security"
    TERRAFORM_DIR = Path("infrastructure/terraform/simulated")

    def __init__(
        self,
        agent_id: str = "agent-security-001",
        name: str = "security-agent",
        db_session=None,
        governance_agent=None,
    ):
        super().__init__(
            agent_id=agent_id,
            name=name,
            db_session=db_session,
            governance_agent=governance_agent,
        )

    async def _execute(self, operation: str, resource: str, **kwargs) -> list[dict]:
        return await self.scan_all()

    async def scan_all(self) -> list[dict]:
        """Run all scanners and return unified findings list."""
        checkov_findings = await self.run_checkov()
        trivy_findings = await self.run_trivy()
        return checkov_findings + trivy_findings

    async def run_checkov(self) -> list[dict]:
        """
        Execute: checkov -d <terraform_dir> -o json
        Parse output and return normalised finding dicts.
        """
        # TODO: subprocess.run checkov, parse JSON, map to FindingSchema
        raise NotImplementedError

    async def run_trivy(self) -> list[dict]:
        """
        Execute: trivy config <terraform_dir> --format json
        Parse output and return normalised finding dicts.
        """
        # TODO: subprocess.run trivy, parse JSON, map to FindingSchema
        raise NotImplementedError

    def _normalise_checkov(self, raw: dict) -> list[dict]:
        """Map Checkov JSON output to internal finding format."""
        raise NotImplementedError

    def _normalise_trivy(self, raw: dict) -> list[dict]:
        """Map Trivy JSON output to internal finding format."""
        raise NotImplementedError
