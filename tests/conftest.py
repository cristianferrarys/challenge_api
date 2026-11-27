import os
os.environ["APP_ENV"] = "testing"

import pytest

from sqlalchemy import text
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.core.config import settings
from app.core.database import Base, engine


@pytest.fixture
async def client():

    # Validar configuración
    if (
        settings.app_env != "testing"
        or engine.url.database != "challenge_test"
        or engine.url.username != "challenge_test"
        or engine.url.port != 5432
        or engine.url.host not in ("localhost", "127.0.0.1")
    ):
        raise RuntimeError("Unsafe testing configuration")

    try:
        async with engine.begin() as conn:

            # Validar conexión real a PostgreSQL
            result = await conn.execute(
                text("SELECT current_database(), current_user")
            )

            database, username = result.one()

            if (
                database != "challenge_test"
                or username != "challenge_test"
            ):
                raise RuntimeError("Unsafe database connection")

            # Crear tablas si no existen
            await conn.run_sync(Base.metadata.create_all)

            # Limpiar registros de testing
            for table in reversed(Base.metadata.sorted_tables):
                await conn.execute(table.delete())

        # Cliente HTTP para los tests
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as test_client:

            yield test_client

    finally:
        await engine.dispose()
