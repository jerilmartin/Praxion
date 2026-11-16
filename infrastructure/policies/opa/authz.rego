# Praxion – Base OPA Authorization Policy
# Package: praxion.authz
# Evaluated by GovernanceAgent for every agent operation.

package praxion.authz

import future.keywords.if
import future.keywords.in

# ── Default deny ─────────────────────────────────────────────────────────────
default allow = false

# ── Allow if agent role permits the operation ─────────────────────────────────
allow if {
    agent_role := data.agents[input.agent_id].role
    permitted_ops := data.role_permissions[agent_role]
    input.operation in permitted_ops
}

# ── Deny suspended agents unconditionally ────────────────────────────────────
allow = false if {
    data.agents[input.agent_id].status == "suspended"
}

# ── High-risk operations always require explicit approval flag ────────────────
requires_approval if {
    input.operation in data.high_risk_operations
}
