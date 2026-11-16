"""
Application factory – creates and configures the FastAPI instance.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.router import api_router
from app.db.session import engine
from app.db.base import Base


def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.APP_NAME,
        version="0.1.0",
        description="Autonomous Cloud Infrastructure Security, Agent Governance and Remediation",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )

    # CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_ORIGIN],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    application.include_router(api_router, prefix="/api/v1")

    @application.on_event("startup")
    async def on_startup():
        # Create tables (dev only; use Alembic in production)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    return application
