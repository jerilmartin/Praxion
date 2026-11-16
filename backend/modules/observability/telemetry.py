"""
Observability Module – OpenTelemetry instrumentation helpers.   (OBJ-6, FR-09)
"""
from __future__ import annotations
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

from app.core.config import settings


def setup_telemetry() -> None:
    """Configure and register global OpenTelemetry TracerProvider."""
    resource = Resource.create({"service.name": settings.OTEL_SERVICE_NAME})
    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT, insecure=True)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)


def get_tracer(name: str = "praxion"):
    return trace.get_tracer(name)


class AgentActivityLogger:
    """
    Records agent actions to the ActivityLog table and emits OTEL spans.
    Use as an async context manager around agent tool calls.
    """

    def __init__(self, agent_id: str, action: str, db_session=None):
        self.agent_id = agent_id
        self.action = action
        self.db = db_session
        self._tracer = get_tracer()
        self._span = None

    async def __aenter__(self):
        self._span = self._tracer.start_span(f"agent.{self.action}")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._span:
            if exc_type:
                self._span.record_exception(exc_val)
            self._span.end()
        # TODO: persist ActivityLog record to DB
