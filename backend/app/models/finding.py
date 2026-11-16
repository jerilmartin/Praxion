"""
SQLAlchemy model – Security Findings   (OBJ-2, FR-02)
"""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, JSON, ForeignKey, Enum as SAEnum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.base import Base


class Severity(str, enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class FindingStatus(str, enum.Enum):
    OPEN = "open"
    REMEDIATED = "remediated"
    ACCEPTED = "accepted"
    FALSE_POSITIVE = "false_positive"


class SecurityFinding(Base):
    __tablename__ = "security_findings"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    resource_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("infrastructure_resources.id"), index=True)
    scanner: Mapped[str] = mapped_column(String(64))          # checkov | trivy | custom
    check_id: Mapped[str] = mapped_column(String(128))
    title: Mapped[str] = mapped_column(String(512))
    description: Mapped[Optional[str]] = mapped_column(Text)
    severity: Mapped[Severity] = mapped_column(SAEnum(Severity))
    status: Mapped[FindingStatus] = mapped_column(SAEnum(FindingStatus), default=FindingStatus.OPEN)
    risk_score: Mapped[Optional[float]] = mapped_column()
    details: Mapped[dict] = mapped_column(JSON, default=dict)
    discovered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    resource = relationship("InfrastructureResource", back_populates="findings")
    remediation_records = relationship("RemediationRecord", back_populates="finding", lazy="dynamic")
