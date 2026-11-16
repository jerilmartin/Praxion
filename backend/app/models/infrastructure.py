"""
SQLAlchemy models – Infrastructure Resources and Relationships   (OBJ-1, FR-01, FR-03)
"""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, JSON, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.base import Base


class ResourceType(str, enum.Enum):
    COMPUTE = "compute"
    STORAGE = "storage"
    DATABASE = "database"
    NETWORK = "network"
    IAM = "iam"
    CONTAINER = "container"
    OTHER = "other"


class ResourceStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    UNKNOWN = "unknown"


class InfrastructureResource(Base):
    __tablename__ = "infrastructure_resources"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    resource_type: Mapped[ResourceType] = mapped_column(SAEnum(ResourceType))
    provider: Mapped[str] = mapped_column(String(64), default="simulated")  # aws | gcp | azure | simulated
    region: Mapped[Optional[str]] = mapped_column(String(64))
    configuration: Mapped[dict] = mapped_column(JSON, default=dict)
    tags: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[ResourceStatus] = mapped_column(SAEnum(ResourceStatus), default=ResourceStatus.ACTIVE)
    discovered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    findings = relationship("SecurityFinding", back_populates="resource", lazy="dynamic")
    outgoing_relations = relationship(
        "ResourceRelationship", foreign_keys="ResourceRelationship.source_id", back_populates="source", lazy="dynamic"
    )
    incoming_relations = relationship(
        "ResourceRelationship", foreign_keys="ResourceRelationship.target_id", back_populates="target", lazy="dynamic"
    )


class ResourceRelationship(Base):
    __tablename__ = "resource_relationships"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id: Mapped[str] = mapped_column(String, ForeignKey("infrastructure_resources.id"), index=True)
    target_id: Mapped[str] = mapped_column(String, ForeignKey("infrastructure_resources.id"), index=True)
    relation_type: Mapped[str] = mapped_column(String(64))   # e.g. "accesses", "contains", "depends_on"
    metadata_: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    source = relationship("InfrastructureResource", foreign_keys=[source_id], back_populates="outgoing_relations")
    target = relationship("InfrastructureResource", foreign_keys=[target_id], back_populates="incoming_relations")
