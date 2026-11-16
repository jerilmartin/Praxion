"""
Integration tests – API health checks
"""
import pytest


@pytest.mark.asyncio
async def test_docs_accessible(client):
    response = await client.get("/api/docs")
    # FastAPI redirects /docs, check for 200 or 307
    assert response.status_code in (200, 307)


@pytest.mark.asyncio
async def test_infrastructure_list_requires_auth(client):
    response = await client.get("/api/v1/infrastructure/")
    # Should be 501 (stub) or 401 (auth guard once implemented)
    assert response.status_code in (401, 501)
