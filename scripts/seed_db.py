"""
Database seed script – populates Praxion with demo data for local development.

Run from the backend/ directory:
    python scripts/seed_db.py

Creates:
    - 1 admin user       (admin / praxion123)
    - 3 AI agents        (discovery, security, remediation)
    - 5 infra resources  (matching the Terraform simulated config)
    - 3 security findings with varying severity
    - 2 OPA policies
"""
from __future__ import annotations
import asyncio
import sys
import os

# Allow running from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings
from app.core.security import get_password_hash
from app.db.base import Base
from app.models.user import User, UserRole
from app.models.agent import Agent, AgentStatus
from app.models.infrastructure import InfrastructureResource, ResourceType, ResourceStatus
from app.models.finding import SecurityFinding, Severity, FindingStatus
from app.models.policy import Policy

engine = create_async_engine(settings.DATABASE_URL, echo=False)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with Session() as db:
        # ── Users ─────────────────────────────────────────────────────────────
        admin = User(
            id="user-admin-001",
            username="admin",
            email="admin@praxion.local",
            hashed_password=get_password_hash("praxion123"),
            role=UserRole.ADMIN,
        )
        db.add(admin)

        # ── Agents ────────────────────────────────────────────────────────────
        agents = [
            Agent(
                id="agent-discovery-001",
                name="discovery-agent",
                role="discovery",
                permissions={"allowed_operations": ["scan_infrastructure", "read_terraform_state"]},
                status=AgentStatus.ACTIVE,
            ),
            Agent(
                id="agent-security-001",
                name="security-agent",
                role="security",
                permissions={"allowed_operations": ["run_checkov", "run_trivy", "write_findings"]},
                status=AgentStatus.ACTIVE,
            ),
            Agent(
                id="agent-remediation-001",
                name="remediation-agent",
                role="remediation",
                permissions={"allowed_operations": ["propose_remediation", "execute_remediation"]},
                status=AgentStatus.ACTIVE,
            ),
        ]
        db.add_all(agents)

        # ── Infrastructure Resources ───────────────────────────────────────────
        resources = [
            InfrastructureResource(
                id="res-compute-001",
                name="web-server-01",
                resource_type=ResourceType.COMPUTE,
                provider="simulated",
                region="us-east-1",
                configuration={"instance_type": "t3.medium", "imdsv2": False},
                tags={"env": "dev", "team": "platform"},
                status=ResourceStatus.ACTIVE,
            ),
            InfrastructureResource(
                id="res-storage-001",
                name="data-bucket-public",
                resource_type=ResourceType.STORAGE,
                provider="simulated",
                region="us-east-1",
                configuration={"public": True, "encryption": "none", "versioning": False},
                tags={"env": "dev"},
                status=ResourceStatus.ACTIVE,
            ),
            InfrastructureResource(
                id="res-iam-001",
                name="app-admin-role",
                resource_type=ResourceType.IAM,
                provider="simulated",
                configuration={"policy": "AdministratorAccess", "mfa_required": False},
                tags={"env": "dev"},
                status=ResourceStatus.ACTIVE,
            ),
            InfrastructureResource(
                id="res-db-001",
                name="app-database-01",
                resource_type=ResourceType.DATABASE,
                provider="simulated",
                region="us-east-1",
                configuration={"encrypted": True, "publicly_exposed": False, "backup_enabled": True},
                tags={"env": "dev"},
                status=ResourceStatus.ACTIVE,
            ),
            InfrastructureResource(
                id="res-net-001",
                name="main-vpc",
                resource_type=ResourceType.NETWORK,
                provider="simulated",
                region="us-east-1",
                configuration={"cidr": "10.0.0.0/16", "flow_logs": False},
                tags={"env": "dev"},
                status=ResourceStatus.ACTIVE,
            ),
        ]
        db.add_all(resources)

        # ── Security Findings ──────────────────────────────────────────────────
        findings = [
            SecurityFinding(
                id="finding-001",
                resource_id="res-storage-001",
                scanner="checkov",
                check_id="CKV_AWS_19",
                title="S3 bucket is not encrypted",
                description="The S3 bucket does not have server-side encryption enabled.",
                severity=Severity.HIGH,
                status=FindingStatus.OPEN,
                risk_score=8.5,
                details={"remediation": "Enable AES-256 or AWS KMS encryption on the bucket."},
            ),
            SecurityFinding(
                id="finding-002",
                resource_id="res-storage-001",
                scanner="checkov",
                check_id="CKV_AWS_20",
                title="S3 bucket has public read access",
                description="The bucket ACL allows public read, exposing data to the internet.",
                severity=Severity.CRITICAL,
                status=FindingStatus.OPEN,
                risk_score=9.8,
                details={"remediation": "Set bucket ACL to private and use pre-signed URLs."},
            ),
            SecurityFinding(
                id="finding-003",
                resource_id="res-iam-001",
                scanner="checkov",
                check_id="CKV_AWS_40",
                title="IAM role has AdministratorAccess policy",
                description="The role grants unrestricted access to all AWS services.",
                severity=Severity.CRITICAL,
                status=FindingStatus.OPEN,
                risk_score=9.5,
                details={"remediation": "Apply least-privilege policy scoped to required actions only."},
            ),
        ]
        db.add_all(findings)

        # ── Policies ──────────────────────────────────────────────────────────
        policies = [
            Policy(
                id="policy-authz-001",
                name="agent-authorization",
                rego_content=open("../infrastructure/policies/opa/authz.rego").read()
                    if os.path.exists("../infrastructure/policies/opa/authz.rego") else
                    "package praxion.authz\ndefault allow = false",
                is_active=True,
            ),
        ]
        db.add_all(policies)

        await db.commit()
        print("✅ Seed complete!")
        print(f"   Admin login: admin / praxion123")
        print(f"   Resources  : {len(resources)}")
        print(f"   Findings   : {len(findings)}")
        print(f"   Agents     : {len(agents)}")


if __name__ == "__main__":
    asyncio.run(seed())
