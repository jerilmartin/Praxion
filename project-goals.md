# Praxion: Autonomous Cloud Infrastructure Security, Agent Governance and Remediation

## Project Goals & Progress

> **Update policy**: This file must be updated after every significant code change.
> Record what was done, what objective it satisfies, and what remains.

---

## Project Overview

**Domain:** Agentic AI, cloud infrastructure security, machine learning and DevSecOps.

**Praxion** is a local-first, AI-powered platform that uses coordinated agents to investigate
cloud infrastructure security risks, assess their impact and propose or carry out controlled
remediation. It combines infrastructure security with governance of the agents that perform
security operations, so their actions are authorized, observable, explainable and accountable.

### Updated Project Goal

Develop a security-governed platform that demonstrates how AI agents can investigate and respond
to cloud infrastructure security issues without receiving unrestricted control over the
infrastructure they manage. The project addresses two linked questions:

1. How can AI agents autonomously investigate and respond to infrastructure security issues?
2. How can the system prevent unauthorized agent actions and detect unexpected or potentially
   unsafe agent behaviour?

The LLM may propose an action, but an external deterministic authorization layer decides whether
the action is permitted. High-impact changes require human approval, are executed through a
controlled layer, and are verified and recorded.

### Project Description

Praxion works against a simulated cloud environment containing resources such as virtual
machines, storage services, networks and IAM policies. Checkov and Trivy identify vulnerabilities
and misconfigurations. Specialized agents investigate findings, use a NetworkX dependency graph
to assess relationships and possible attack paths, and develop remediation plans.

Open Policy Agent (OPA) evaluates sensitive tool calls against policy before execution. Machine
learning based behavioural monitoring (Isolation Forest) identifies unusual activity and can raise
alerts or trigger additional safeguards; it does not grant or revoke permissions. For high-impact
remediation, the system requests human approval, executes approved changes through a controlled
layer, verifies the outcome and records an audit trail. A centralized dashboard is intended to
show infrastructure risks, agent decisions, authorization outcomes, anomalies and remediation
history.

### Research Focus and Contribution

The central contribution is the integration of infrastructure security automation with security
governance of the agents performing it. The project does not claim to invent vulnerability
scanning, attack-path analysis, AI remediation or anomaly detection individually. Its contribution
is an engineering and research demonstration of how these capabilities can work together under
external authorization, behavioural monitoring, adversarial evaluation and accountable remediation.

The work is organized around three pillars:

1. **Intelligent infrastructure security:** discovery, scanning, dependency graphs, risk
   investigation and remediation planning.
2. **AI agent security and governance:** least-privilege tool access, OPA authorization,
   behavioural anomaly detection and adversarial agent testing.
3. **Controlled autonomous remediation:** human approval, safe execution, post-change
   verification and auditability.

Graph analysis provides resource relationships and potential impact; it is not itself AI. OPA
enforces individual operation permissions, while behavioural monitoring looks for patterns across
agent activity. These controls complement each other, and the ML model never replaces OPA's
authorization decision.

---

## Objectives Tracker

| ID | Objective | Status | Notes |
|----|-----------|--------|-------|
| OBJ-1 | Simulated cloud infrastructure environment | 🟡 Skeleton | `infrastructure/terraform/simulated/main.tf` created with intentional misconfigs |
| OBJ-2 | Specialized AI agents (discovery, scan, remediation) | 🟡 Skeleton | Agent classes stubbed; `NotImplementedError` on all methods |
| OBJ-3 | Infrastructure dependency graph + attack paths | 🟡 Skeleton | `InfrastructureGraph` class built with NetworkX; pending DB integration |
| OBJ-4 | Agent identity, least-privilege permissions + OPA authorization | 🟡 Skeleton | `GovernanceAgent` + `OPAPolicyClient` stubbed; Rego policy written; authorization is the deterministic enforcement layer |
| OBJ-5 | Adversarial agent testing + ML behavioural anomaly detection | 🟡 Skeleton | `AttackSimulator` + `AnomalyDetectionAgent` stubbed; training script ready; ML flags unusual patterns but does not authorize actions |
| OBJ-6 | Centralized observability / dashboard | 🟡 Skeleton | OpenTelemetry helpers stubbed; frontend pages not yet created |
| OBJ-7 | Controlled remediation with human approval, execution verification and auditability | 🟡 Skeleton | Approval + Remediation models and endpoints stubbed |

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
| FR-10 | Detect and record adversarial attempts against agents (including unauthorized access, privilege escalation, prompt injection, excessive tool use and cross-agent misuse) | 🟡 Simulator + endpoint stubbed; 4 scenarios defined |
| FR-11 | Require approval for sensitive remediation, execute approved changes through a controlled layer, and verify outcomes | 🟡 Approval + Remediation models and endpoints stubbed |
| FR-12 | Evaluate end-to-end effectiveness: blocked unauthorized actions, detected anomalies, graph-based impact assessment, approval enforcement and successful remediation verification | 🔴 Evaluation criteria defined; measurement and experiments pending |

---

## Changelog

### 2026-11-25 — BaseAgent Iteration 1

**What was done:**
- Made the shared `_execute()` contract explicit for operation and resource context.
- Kept authorization fail-closed and convert governance errors into policy denials.
- Fixed `SecurityScanAgent` initialization so it calls `BaseAgent.__init__()`.

**Remaining:** Activity-log transaction behavior and authorization-decision logging are for iteration 2.

### 2026-11-23 — Updated Project Goal and Research Focus

**What was done:**
- Reframed Praxion around the combined problem of infrastructure security and governance of the AI agents performing security operations.
- Documented the three research pillars: intelligent infrastructure security, agent security and governance, and controlled autonomous remediation.
- Clarified the distinct roles of OPA authorization, ML behavioural monitoring, graph analysis, human approval, controlled execution and post-remediation verification.
- Added functional requirements for adversarial agent testing, controlled verified remediation and measurable evaluation.

**Objective satisfied:** Aligns the project goals and requirements with the updated project description and makes the intended contribution and evaluation focus explicit.

### 2026-11-16 — Useful Additions (Session 2)

**What was done:**
- **29 `__init__.py` files** created across all Python packages — the project was unimportable without them
- **`alembic.ini`** (`backend/`) — required for `alembic upgrade head` to find the migration env
- **`pyproject.toml`** (project root) — unified config for pytest (asyncio-auto, coverage), black, ruff, mypy; replaces scattered `.cfg` files
- **`app/api/v1/endpoints/health.py`** — `GET /health` liveness probe + `GET /` root; wired into `application.py`
- **`app/core/deps.py`** — reusable FastAPI `Depends()` helpers: `DBSession`, `Pagination` (skip/limit), `CurrentUserId` (JWT decode)
- **`app/core/exceptions.py`** — domain exception hierarchy (`NotFoundError`, `ForbiddenError`, `PolicyViolationError`, `ConflictError`) + FastAPI handlers registered in app factory
- **`app/schemas/common.py`** — shared Pydantic envelopes: `PaginatedResponse[T]`, `MessageResponse`, `ErrorResponse`, `IDResponse`
- **`app/db/repository.py`** — generic async `BaseRepository[ModelT]` with `get`, `get_or_404`, `list`, `create`, `update`, `delete`
- **`agents/base_agent.py`** — abstract `BaseAgent` with built-in OPA authorization gate, timing, structured logging, and activity-log hook; `InfrastructureDiscoveryAgent` and `SecurityScanAgent` now inherit from it
- **`scripts/seed_db.py`** — runnable seed script: 1 admin user, 3 agents, 5 infra resources, 3 findings, 1 policy

**Files modified:**
- `app/core/application.py` — registers `health_router` and `register_exception_handlers`
- `agents/discovery/discovery_agent.py` — inherits `BaseAgent`
- `agents/security/security_agent.py` — inherits `BaseAgent`

### 2026-11-16 — Initial Skeletal Structure (Session 1)

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
