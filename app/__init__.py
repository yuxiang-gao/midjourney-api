import sys

from loguru import logger

from app.settings import settings

# logger config

log_format = (
    "<green>{time:%Y-%m-%d %H:%M:%S}</> | "
    + "<level>{level}</> | "
    + "{process.id}-{thread.id} | "
    + '"{file.path}:{line}":<blue>{function}</> '
    + "- <level>{message}</>"
)
logger.remove()
logger.add(
    sys.stdout,
    level=settings.log_level,
    format=log_format,
    colorize=True,
)

logger.add(
    f"log/mj-api.log",
    level=settings.log_level,
    format=log_format,
    rotation="00:00",
    retention="3 days",
    backtrace=True,
    diagnose=True,
    enqueue=True,
)
