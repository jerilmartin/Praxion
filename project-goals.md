# Praxion – Project Goals & Progress

> **Update policy**: This file must be updated after every significant code change.
> Record what was done, what objective it satisfies, and what remains.

---

## Project Overview

**Praxion** is a local-first, multi-agent AI platform for autonomous cloud infrastructure security,
agent governance and controlled remediation.

---

## Objectives Tracker

| ID | Objective | Status | Notes |
|----|-----------|--------|-------|
| OBJ-1 | Simulated cloud infrastructure environment | 🟡 Skeleton | `infrastructure/terraform/simulated/main.tf` created with intentional misconfigs |
| OBJ-2 | Specialized AI agents (discovery, scan, remediation) | 🟡 Skeleton | Agent classes stubbed; `NotImplementedError` on all methods |
| OBJ-3 | Infrastructure dependency graph + attack paths | 🟡 Skeleton | `InfrastructureGraph` class built with NetworkX; pending DB integration |
| OBJ-4 | Agent identity management + OPA authorization | 🟡 Skeleton | `GovernanceAgent` + `OPAPolicyClient` stubbed; Rego policy written |
| OBJ-5 | Attack simulation + ML anomaly detection | 🟡 Skeleton | `AttackSimulator` + `AnomalyDetectionAgent` stubbed; training script ready |
| OBJ-6 | Centralized observability / dashboard | 🟡 Skeleton | OpenTelemetry helpers stubbed; frontend pages not yet created |
| OBJ-7 | Controlled remediation with human approval | 🟡 Skeleton | Approval + Remediation models and endpoints stubbed |

---

## Functional Requirements Tracker

| ID | Requirement | Status |
|----|-------------|--------|
| FR-01 | Discover and maintain resource inventory | 🟡 Endpoint + model created; discovery logic TODO |
| FR-02 | Scan configurations and identify findings | 🟡 Endpoint + scanner wrappers stubbed |
| FR-03 | Represent resource relationships and attack paths | 🟡 Graph module built; endpoint returns 501 |
| FR-04 | Register agents and assign roles/permissions | 🟡 Model + endpoint stubbed |
| FR-05 | Evaluate operations against authorization policies | 🟡 OPA client + Rego policy written; wired to governance agent |
| FR-06 | Simulate agent attacks and record outcomes | 🟡 Simulator + endpoint stubbed; 4 scenarios defined |
| FR-07 | ML-based anomaly detection | 🟡 Agent stubbed; training script complete |
| FR-08 | Human approval/rejection workflow | 🟡 Model + endpoints stubbed |
| FR-09 | Activity logs and execution results | 🟡 Model + endpoint stubbed; OTEL helpers ready |

---

## Changelog

### 2026-11-16 — Initial Skeletal Structure

**What was done:**
- Created full directory tree (32 directories)
- `requirements.txt` with pinned versions for all 7 tech domains
- `.env.example`, `.gitignore`
- **Backend** (`backend/`)
  - `main.py` → FastAPI entry point
  - `app/core/` → `config.py`, `security.py` (JWT + bcrypt), `application.py`
  - `app/db/` → `session.py` (async SQLAlchemy), `base.py`, `migrations_env.py`
  - `app/models/` → 10 ORM models: User, Agent, InfrastructureResource, ResourceRelationship, SecurityFinding, Policy, ActivityLog, AnomalyRecord, ApprovalRequest, RemediationRecord
  - `app/api/v1/` → `router.py` + 11 endpoint modules (all stubbed with 501)
  - `agents/` → 6 agent classes (orchestrator, discovery, security, remediation, governance, anomaly) — all methods stubbed
  - `modules/` → graph, policy (OPA client), scanning (Checkov/Trivy CLI), simulation (4 scenarios), observability (OTEL)
- **Infrastructure**
  - `terraform/simulated/main.tf` — 5 simulated resources with intentional misconfigs
  - `policies/opa/authz.rego` — base OPA authorization policy
- **ML**
  - `ml/anomaly_detection/train.py` — Isolation Forest training script (runnable)
- **Docker**
  - `docker-compose.yml` — PostgreSQL, OPA, Backend, Frontend, OTel Collector
  - `Dockerfile.backend`, `Dockerfile.frontend`, `otel-collector-config.yaml`
- **Tests**
  - `conftest.py`, `test_graph.py`, `test_anomaly.py`, `test_api.py`, `test_attack_simulation.py`
- **Scripts**
  - `setup.sh` (Linux/macOS), `setup.ps1` (Windows)
- `README.md`, `project-goals.md`

**Objectives satisfied (partially):** OBJ-1 through OBJ-7 (skeleton level)

---

## Next Steps (Phase 1 → Phase 2)

### Immediate (Phase 1 completion)
- [ ] `InfrastructureDiscoveryAgent.discover()` — parse Terraform state/output
- [ ] `SecurityScanAgent.run_checkov()` / `run_trivy()` — real subprocess calls + result normalisation
- [ ] `InfrastructureGraph.build_from_db()` — wire to DB query
- [ ] Pydantic schemas (`app/schemas/`) for all endpoints
- [ ] Alembic initial migration (`alembic revision --autogenerate -m "initial"`)

### Phase 2
- [ ] `GovernanceAgent.authorize()` — full OPA integration with decision logging
- [ ] `OrchestratorAgent` — LangGraph `StateGraph` wiring all 8 nodes
- [ ] Auth middleware — JWT dependency on all protected endpoints

### Phase 3
- [ ] `AnomalyDetectionAgent.score()` — live scoring from DB
- [ ] `AttackSimulator` — implement all 4 scenario handlers
- [ ] React frontend — dashboard pages: Findings, Graph, Agents, Approvals, Logs

### Phase 4
- [ ] `RemediationPlannerAgent` — LLM-based proposal generation
- [ ] Human-in-the-loop interrupt in LangGraph orchestrator
- [ ] End-to-end integration tests

### Phase 5–6
- [ ] Performance tuning, documentation, evaluation against OWASP Top 10 for Agentic AI
- [ ] Final demo scenarios and report

---

## Status Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Complete |
| 🟡 | Skeleton / Stub |
| 🔴 | Not started |
| 🔵 | In progress |
