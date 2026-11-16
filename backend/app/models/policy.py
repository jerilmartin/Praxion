"""
SQLAlchemy models – Policies, Activity Logs, Anomalies, Approvals, Remediations
"""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, JSON, ForeignKey, Enum as SAEnum, Text, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.base import Base


# ── Policies ─────────────────────────────────────────────────────────────────

class Policy(Base):
    __tablename__ = "policies"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    rego_content: Mapped[str] = mapped_column(Text, nullable=False)   # OPA Rego policy
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ── Activity Logs ─────────────────────────────────────────────────────────────

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("agents.id"), index=True)
    action: Mapped[str] = mapped_column(String(255))                    # tool name or operation
    input_data: Mapped[dict] = mapped_column(JSON, default=dict)
    output_data: Mapped[dict] = mapped_column(JSON, default=dict)
    authorized: Mapped[Optional[bool]] = mapped_column(Boolean)
    execution_time_ms: Mapped[Optional[float]] = mapped_column(Float)
    error: Mapped[Optional[str]] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    agent = relationship("Agent", back_populates="activity_logs")


# ── Anomaly Records ───────────────────────────────────────────────────────────

class AnomalyRecord(Base):
    __tablename__ = "anomaly_records"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id: Mapped[str] = mapped_column(String, ForeignKey("agents.id"), index=True)
    anomaly_score: Mapped[float] = mapped_column(Float)
    is_anomalous: Mapped[bool] = mapped_column(Boolean)
    features: Mapped[dict] = mapped_column(JSON, default=dict)          # input features used
    details: Mapped[Optional[str]] = mapped_column(Text)
    detected_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    agent = relationship("Agent", back_populates="anomaly_records")


# ── Approval Requests ─────────────────────────────────────────────────────────

class ApprovalStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class ApprovalRequest(Base):
    __tablename__ = "approval_requests"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    operation: Mapped[str] = mapped_column(String(255), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    requested_by_agent_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("agents.id"))
    reviewer_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("users.id"))
    status: Mapped[ApprovalStatus] = mapped_column(SAEnum(ApprovalStatus), default=ApprovalStatus.PENDING)
    reviewer_notes: Mapped[Optional[str]] = mapped_column(Text)
    requested_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    reviewer = relationship("User", back_populates="approval_requests")


# ── Remediation Records ───────────────────────────────────────────────────────

class RemediationStatus(str, enum.Enum):
    PROPOSED = "proposed"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    REJECTED = "rejected"


class RemediationRecord(Base):
    __tablename__ = "remediation_records"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    finding_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("security_findings.id"), index=True)
    approval_request_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("approval_requests.id"))
    proposed_action: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[RemediationStatus] = mapped_column(SAEnum(RemediationStatus), default=RemediationStatus.PROPOSED)
    execution_result: Mapped[Optional[dict]] = mapped_column(JSON)
    verification_result: Mapped[Optional[dict]] = mapped_column(JSON)
    proposed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    executed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    finding = relationship("SecurityFinding", back_populates="remediation_records")
