import asyncio

from arq.connections import ArqRedis, RedisSettings, create_pool
from loguru import logger

from app.settings import settings

from .tasks import generate, shutdown, startup

redis_settings = RedisSettings.from_dsn(str(settings.redis_dsn))


class WorkerSettings:
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = redis_settings
    functions: list = [generate]
    timezone = settings.timezone
    max_jobs = settings.worker_max_jobs
    keep_result = settings.worker_keep_result_s
    max_tries = settings.max_tries
