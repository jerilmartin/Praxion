"""
SQLAlchemy model – AI Agents   (OBJ-4, FR-04, FR-05)
"""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, JSON, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.base import Base


class AgentStatus(str, enum.Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DECOMMISSIONED = "decommissioned"


class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(64), nullable=False)           # e.g. "discovery", "remediation"
    permissions: Mapped[dict] = mapped_column(JSON, default=dict)           # allowed tools / resources
    status: Mapped[AgentStatus] = mapped_column(SAEnum(AgentStatus), default=AgentStatus.ACTIVE)
    metadata_: Mapped[Optional[dict]] = mapped_column("metadata", JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    activity_logs = relationship("ActivityLog", back_populates="agent", lazy="dynamic")
    anomaly_records = relationship("AnomalyRecord", back_populates="agent", lazy="dynamic")
