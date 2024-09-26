from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config.settings import settings
from app.db.models import Base

DATABASE_URL = settings.db

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async_engine = create_async_engine(DATABASE_URL, echo=False)


async def get_session() -> AsyncGenerator[AsyncSession, Any]:
    async with async_session() as session:
        await session.begin()
        yield session
        await session.close()


async def init_models() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
