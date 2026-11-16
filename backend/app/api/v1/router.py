"""
Top-level API router – aggregates all v1 endpoints.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    infrastructure,
    findings,
    agents,
    policies,
    logs,
    anomalies,
    approvals,
    remediation,
    graph,
    simulation,
)

api_router = APIRouter()

api_router.include_router(auth.router,           prefix="/auth",           tags=["Auth"])
api_router.include_router(infrastructure.router, prefix="/infrastructure",  tags=["Infrastructure"])
api_router.include_router(findings.router,       prefix="/findings",        tags=["Findings"])
api_router.include_router(agents.router,         prefix="/agents",          tags=["Agents"])
api_router.include_router(policies.router,       prefix="/policies",        tags=["Policies"])
api_router.include_router(logs.router,           prefix="/logs",            tags=["Logs"])
api_router.include_router(anomalies.router,      prefix="/anomalies",       tags=["Anomalies"])
api_router.include_router(approvals.router,      prefix="/approvals",       tags=["Approvals"])
api_router.include_router(remediation.router,    prefix="/remediation",     tags=["Remediation"])
api_router.include_router(graph.router,          prefix="/graph",           tags=["Graph"])
api_router.include_router(simulation.router,     prefix="/simulation",      tags=["Simulation"])
