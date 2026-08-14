import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Load DATABASE_URL (and friends) from the repo-root .env file.
# In containers, real env vars are already set and this is a no-op.
load_dotenv(Path(__file__).resolve().parents[3] / ".env")

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_async_engine(DATABASE_URL)

# expire_on_commit=False so ORM objects stay usable after commit,
# which is convenient for returning them straight from FastAPI endpoints.
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncSession:
    """FastAPI dependency that yields a request-scoped async session."""
    async with async_session_maker() as session:
        yield session
