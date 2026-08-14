import os
from collections.abc import AsyncGenerator

import asyncpg
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.base import Base
from app.db.session import DATABASE_URL, get_db
from app.main import app

# Use a dedicated database on the same Postgres instance so tests never
# touch dev data.
TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL", DATABASE_URL.rsplit("/", 1)[0] + "/sentinel_test"
)


async def _ensure_test_database_exists() -> None:
    # asyncpg.connect() needs a plain "postgresql://" URL, not "+asyncpg".
    plain_url = TEST_DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    db_name = plain_url.rsplit("/", 1)[-1]
    admin_url = plain_url.rsplit("/", 1)[0] + "/postgres"

    conn = await asyncpg.connect(admin_url)
    try:
        exists = await conn.fetchval("SELECT 1 FROM pg_database WHERE datname = $1", db_name)
        if not exists:
            await conn.execute(f'CREATE DATABASE "{db_name}"')
    finally:
        await conn.close()


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession]:
    await _ensure_test_database_exists()

    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    async with session_maker() as session:
        yield session
        # Keep the test database clean between tests.
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()

    await engine.dispose()


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient]:
    async def _override_get_db() -> AsyncGenerator[AsyncSession]:
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
