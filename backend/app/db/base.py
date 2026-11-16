"""
SQLAlchemy declarative base – import all models here so Alembic sees them.
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import all models so their tables are registered
from app.models import (  # noqa: F401, E402
    user,
    agent,
    infrastructure,
    finding,
    policy,
    activity_log,
    anomaly,
    approval,
    remediation,
)
