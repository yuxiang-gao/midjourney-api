import platform
from datetime import tzinfo
from pathlib import Path
from typing import Literal

from dateutil.tz import gettz
from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    fastapi_root_path: str = ""
    redis_dsn: RedisDsn = RedisDsn("redis://redis:6379/0")

    # discord related
    user_token: str
    bot_token: str
    guild_id: int
    channel_id: int

    discord_base_url: str = "https://discord.com/api/v9"

    # task queue
    timezone: tzinfo | None = gettz("Asia/Shanghai")
    worker_max_jobs: int = 3
    worker_keep_result_s: int = 60 * 60 * 6  # 6 hours
    pool_type: Literal["thread", "process"] = "process"
    pool_max_workers: int = 6
    retry_defer: float = 5.0  # seconds
    max_tries: int = 3  # times
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "ERROR"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()  # type: ignore
print(settings.model_dump())
