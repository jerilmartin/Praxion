# Praxion

**Autonomous Cloud Infrastructure Security, Agent Governance and Remediation**

> Local-first · Multi-Agent AI · Policy-Based Authorization · ML Anomaly Detection

---

## Quick Start

```powershell
# Windows
.\.venv\Scripts\Activate.ps1
.\scripts\setup.ps1
```

```bash
# Linux / macOS / WSL2
source .venv/bin/activate
bash scripts/setup.sh
```

Then open:
- **API docs** → http://localhost:8000/api/docs
- **Dashboard** → http://localhost:3000

---

## Project Structure

```
Praxion/
├── backend/
│   ├── main.py                          # FastAPI entry point
│   ├── app/
│   │   ├── api/v1/endpoints/            # REST endpoints (11 modules)
│   │   ├── core/                        # Config, security, app factory
│   │   ├── db/                          # SQLAlchemy engine, session, base, migrations
│   │   ├── models/                      # 10 ORM models
│   │   ├── schemas/                     # Pydantic request/response schemas (TODO)
│   │   └── services/                    # Business logic services (TODO)
│   ├── agents/
│   │   ├── orchestrator/                # LangGraph master orchestrator
│   │   ├── discovery/                   # Infrastructure discovery agent
│   │   ├── security/                    # Checkov + Trivy scan agent
│   │   ├── remediation/                 # Planner + executor agents
│   │   ├── governance/                  # Agent identity + OPA authorization
│   │   └── anomaly/                     # Isolation Forest anomaly detection
│   └── modules/
│       ├── graph/                       # NetworkX dependency graph
│       ├── policy/                      # OPA REST client
│       ├── scanning/                    # Checkov / Trivy CLI wrappers
│       ├── simulation/                  # Attack simulator
│       └── observability/               # OpenTelemetry helpers
├── infrastructure/
│   ├── terraform/simulated/main.tf      # Simulated cloud resources
│   └── policies/opa/authz.rego         # OPA authorization policy
├── frontend/src/                        # React dashboard (TODO)
├── ml/
│   ├── anomaly_detection/train.py       # IsolationForest training script
│   └── models/                          # Saved model artifacts
├── docker/                              # Dockerfiles + OTel config
├── tests/
│   ├── unit/                            # Graph, anomaly unit tests
│   ├── integration/                     # API integration tests
│   └── simulation/                      # Attack simulation tests
├── scripts/                             # setup.sh / setup.ps1
├── requirements.txt
├── docker-compose.yml
└── project-goals.md
```

---

## Modules

| # | Module | Key Technologies |
|---|--------|-----------------|
| 1 | Infrastructure Discovery & Security Analysis | Terraform, Checkov, Trivy |
| 2 | Infrastructure Risk & Dependency Graph | NetworkX |
| 3 | AI-Agent Governance & Authorization | LangGraph, OPA (Rego) |
| 4 | Agent Security Testing & Attack Simulation | Custom scenarios |
| 5 | Agent Behavioural Anomaly Detection | scikit-learn Isolation Forest |
| 6 | Agent Activity & Operational Observability | OpenTelemetry, FastAPI |
| 7 | Controlled Remediation & Human Approval | LangGraph interrupt, PostgreSQL |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12 |
| Agent Framework | LangGraph |
| LLM | Gemini API / Ollama |
| Backend | FastAPI + SQLAlchemy (async) |
| Database | PostgreSQL 16 |
| Policy Engine | Open Policy Agent |
| Graph Analysis | NetworkX |
| ML | scikit-learn (Isolation Forest) |
| IaC | Terraform (simulated) |
| Scanning | Checkov, Trivy |
| Observability | OpenTelemetry |
| Frontend | React |
| Deployment | Docker Compose |

---

## Running Tests

```bash
pytest tests/ -v --cov=backend
```
