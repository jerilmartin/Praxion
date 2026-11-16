"""
Simulation tests – verify attack scenarios are detected / blocked
"""
import pytest

SCENARIOS = [
    "unauthorized_tool_access",
    "privilege_escalation",
    "prompt_injection",
    "agent_communication_abuse",
]


@pytest.mark.parametrize("scenario", SCENARIOS)
@pytest.mark.asyncio
async def test_simulation_scenario_runs(client, scenario):
    """Each scenario endpoint should respond (501 until implemented)."""
    response = await client.post(f"/api/v1/simulation/run/{scenario}")
    assert response.status_code in (200, 501)
