"""
Abstract base class for all Praxion agents.

Every agent (discovery, security, governance, remediation, anomaly) inherits
from BaseAgent, gaining:
  - structured logging via AgentActivityLogger
  - automatic OPA authorization check before running
  - run-time metadata (name, role, agent_id)
"""
from __future__ import annotations
import abc
import logging
import time
from typing import Any, Optional

logger = logging.getLogger(__name__)


class BaseAgent(abc.ABC):
    """
    Abstract base class all Praxion agents must extend.

    Subclasses implement:
        async def _execute(self, **kwargs) -> Any

    Callers use:
        result = await agent.run(**kwargs)
    """

    #: Override in each subclass, e.g. "discovery", "security"
    agent_role: str = "base"

    def __init__(
        self,
        agent_id: str,
        name: str,
        db_session=None,
        governance_agent=None,
    ):
        self.agent_id = agent_id
        self.name = name
        self.db = db_session
        self.governance = governance_agent
        self._logger = logging.getLogger(f"praxion.agent.{self.agent_role}")

    # ── Public interface ──────────────────────────────────────────────────────

    async def run(self, operation: str, resource: str = "*", **kwargs) -> Any:
        """
        Authorise then execute the agent's main logic.

        Args:
            operation: Named operation (used for OPA check), e.g. "scan_infrastructure"
            resource:  Target resource identifier
            **kwargs:  Passed through to _execute()
        """
        # 1. Authorization gate
        allowed = await self._check_authorization(operation, resource)
        if not allowed:
            from app.core.exceptions import PolicyViolationError
            raise PolicyViolationError(
                f"Agent '{self.name}' is not permitted to perform '{operation}' on '{resource}'"
            )

        # 2. Execute with timing
        start = time.monotonic()
        try:
            self._logger.info("Agent '%s' starting '%s'", self.name, operation)
            result = await self._execute(operation=operation, resource=resource, **kwargs)
            elapsed_ms = (time.monotonic() - start) * 1000
            self._logger.info(
                "Agent '%s' completed '%s' in %.1fms", self.name, operation, elapsed_ms
            )
            await self._log_activity(
                operation, {"resource": resource, **kwargs}, result, elapsed_ms, error=None
            )
            return result
        except Exception as exc:
            elapsed_ms = (time.monotonic() - start) * 1000
            self._logger.error("Agent '%s' failed '%s': %s", self.name, operation, exc)
            await self._log_activity(
                operation, {"resource": resource, **kwargs}, {}, elapsed_ms, error=str(exc)
            )
            raise

    # ── Abstract method – subclasses implement this ───────────────────────────

    @abc.abstractmethod
    async def _execute(self, **kwargs) -> Any:
        """Core agent logic. Called only after authorization succeeds."""
        ...

    # ── Helpers ───────────────────────────────────────────────────────────────

    async def _check_authorization(self, operation: str, resource: str) -> bool:
        """Only run an agent operation when governance approves it."""
        if self.governance is None:
            self._logger.warning("No governance agent wired – denying '%s'", operation)
            return False
        return await self.governance.authorize(self.agent_id, operation, resource)

    async def _log_activity(
        self,
        action: str,
        input_data: dict,
        output_data: Any,
        elapsed_ms: float,
        error: Optional[str],
    ) -> None:
        """Add an activity record to the current database transaction."""
        if self.db is None:
            return

        from app.models.policy import ActivityLog

        record = ActivityLog(
            agent_id=self.agent_id,
            action=action,
            input_data=input_data,
            output_data=output_data if isinstance(output_data, dict) else {"result": output_data},
            authorized=True,
            execution_time_ms=elapsed_ms,
            error=error,
        )
        self.db.add(record)
        await self.db.flush()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.agent_id!r} name={self.name!r}>"
