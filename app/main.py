import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any

from redis import asyncio as aioredis
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.api.router import api_router
from app.config.settings import settings, logging_settings
from app.db.config import init_models
from app.middlewares.middelwares import LoggingBadRequestMiddleware

logging.basicConfig(
    level=logging_settings.logging_lvl,
    format=logging_settings.format,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, None]:  # noqa: ARG001
    redis = aioredis.from_url(settings.redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    await init_models()
    yield


app = FastAPI(
    lifespan=lifespan,
    title=settings.app_name,
    description=settings.description,
    version=settings.version,
)

app.include_router(api_router)
app.add_middleware(LoggingBadRequestMiddleware)
