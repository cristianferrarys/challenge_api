import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.core.database import Base, engine


@pytest.fixture
async def client():
    # Protección contra eliminación accidental de datos.
    if engine.url.database != "challenge_test":
        raise RuntimeError(
            "Tests must use challenge_test database"
        )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as test_client:
            yield test_client

    finally:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()
