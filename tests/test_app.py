import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
import app.main as main


@pytest.mark.asyncio
async def test_openapi_schema():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        response = await client.get("/openapi.json")

    assert response.status_code == 200
    assert "paths" in response.json()


@pytest.mark.asyncio
async def test_health_check():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        response = await client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "UP"
    assert response.json()["database"] == "MongoDB connected"


@pytest.mark.asyncio
async def test_health_check_database_failure(monkeypatch):
    from types import SimpleNamespace
    from unittest.mock import AsyncMock

    mock_client = SimpleNamespace(
        admin=SimpleNamespace(
            command=AsyncMock(side_effect=Exception("Database unavailable"))
        )
    )

    monkeypatch.setattr(main, "client", mock_client)

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        response = await client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "DOWN"
    assert response.json()["database"] == "MongoDB connection failed"
    assert response.json()["error"] == "Database unavailable"


@pytest.mark.asyncio
async def test_register_user():
    from pymongo import AsyncMongoClient
    from app.config.settings import settings
    import app.repositories.user_repository as user_repository_module

    test_client = AsyncMongoClient(settings.mongo_uri)
    test_db = test_client[settings.database_name]

    original_db = user_repository_module.db
    user_repository_module.db = test_db

    user_data = {
        "name": "Test Customer",
        "email": "pytest_customer_001@example.com",
        "password": "Test@123456"
    }

    try:
        await test_db.users.delete_one({
            "email": user_data["email"]
        })

        transport = ASGITransport(app=app)

        async with AsyncClient(
            transport=transport,
            base_url="http://test"
        ) as client:
            response = await client.post(
                "/api/v1/auth/register",
                json=user_data
            )

        assert response.status_code == 201
        assert response.json()["email"] == user_data["email"]
        assert response.json()["name"] == user_data["name"]

    finally:
        user_repository_module.db = original_db
        await test_client.close()

@pytest.mark.asyncio
async def test_login_user():
    from pymongo import AsyncMongoClient
    from app.config.settings import settings
    import app.repositories.user_repository as user_repository_module

    test_client = AsyncMongoClient(settings.mongo_uri)
    test_db = test_client[settings.database_name]

    original_db = user_repository_module.db
    user_repository_module.db = test_db

    user_data = {
        "name": "Login Test User",
        "email": "pytest_login_001@example.com",
        "password": "Test@123456"
    }

    try:
        await test_db.users.delete_one({
            "email": user_data["email"]
        })

        transport = ASGITransport(app=app)

        async with AsyncClient(
            transport=transport,
            base_url="http://test"
        ) as client:

            register_response = await client.post(
                "/api/v1/auth/register",
                json=user_data
            )

            assert register_response.status_code == 201

            login_response = await client.post(
                "/api/v1/auth/login",
                json={
                    "email": user_data["email"],
                    "password": user_data["password"]
                }
            )

        assert login_response.status_code == 200
        assert "access_token" in login_response.json()
        assert login_response.json()["token_type"] == "bearer"

    finally:
        user_repository_module.db = original_db
        await test_client.close()


@pytest.mark.asyncio
async def test_login_wrong_password():
    from pymongo import AsyncMongoClient
    from app.config.settings import settings
    import app.repositories.user_repository as user_repository_module

    test_client = AsyncMongoClient(settings.mongo_uri)
    test_db = test_client[settings.database_name]

    original_db = user_repository_module.db
    user_repository_module.db = test_db

    user_data = {
        "name": "Wrong Password Test",
        "email": "pytest_wrong_password@example.com",
        "password": "Correct@123"
    }

    try:
        await test_db.users.delete_one({
            "email": user_data["email"]
        })

        transport = ASGITransport(app=app)

        async with AsyncClient(
            transport=transport,
            base_url="http://test"
        ) as client:
            register_response = await client.post(
                "/api/v1/auth/register",
                json=user_data
            )
            assert register_response.status_code == 201

            login_response = await client.post(
                "/api/v1/auth/login",
                json={
                    "email": user_data["email"],
                    "password": "Wrong@123"
                }
            )

        assert login_response.status_code == 401

    finally:
        user_repository_module.db = original_db
        await test_client.close()

@pytest.mark.asyncio
async def test_register_duplicate_email():
    from pymongo import AsyncMongoClient
    from app.config.settings import settings
    import app.repositories.user_repository as user_repository_module

    test_client = AsyncMongoClient(settings.mongo_uri)
    test_db = test_client[settings.database_name]

    original_db = user_repository_module.db
    user_repository_module.db = test_db

    user_data = {
        "name": "Duplicate Test User",
        "email": "pytest_duplicate@example.com",
        "password": "Test@123456"
    }

    try:
        await test_db.users.delete_one({
            "email": user_data["email"]
        })

        transport = ASGITransport(app=app)

        async with AsyncClient(
            transport=transport,
            base_url="http://test"
        ) as client:
            first_response = await client.post(
                "/api/v1/auth/register",
                json=user_data
            )

            second_response = await client.post(
                "/api/v1/auth/register",
                json=user_data
            )

        assert first_response.status_code == 201
        assert second_response.status_code == 409

    finally:
        user_repository_module.db = original_db
        await test_client.close()


@pytest.mark.asyncio
async def test_global_exception_handler():
    from fastapi import APIRouter

    test_router = APIRouter()

    @test_router.get("/test-unexpected-error")
    async def trigger_unexpected_error():
        raise RuntimeError("Sensitive internal details")

    app.include_router(test_router)

    transport = ASGITransport(
        app=app,
        raise_app_exceptions=False
    )

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        response = await client.get("/test-unexpected-error")

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Internal server error"
    }