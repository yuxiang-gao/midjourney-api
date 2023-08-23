import asyncio
import random
from contextlib import asynccontextmanager
from uuid import uuid4

from arq.connections import ArqRedis, create_pool
from arq.jobs import Job, JobStatus
from fastapi import APIRouter, Body, FastAPI, HTTPException, Query, Security, status
from loguru import logger

from app.discord.bot import bot
from app.discord.enums import TriggerType
from app.settings import settings
from app.tasks.worker import redis_settings

from .models import *

context = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await bot.start(settings.bot_token)
    await bot.login(settings.bot_token)
    logger.info(f"Discord bot logged in: {bot.user}")
    asyncio.create_task(bot.connect(reconnect=True))

    context["redis"] = await create_pool(redis_settings)
    logger.info(f"ARQ pool created: {context['redis']}")
    yield
    await bot.close()
    await context["redis"].close()
    logger.info(f"ARQ pool closed: {context['redis']}")


router = APIRouter(prefix="/api", tags=["api"])


@router.post("/imagine")
async def imagine(body: TaskImagine) -> TaskResponse:
    queue: ArqRedis = context["redis"]
    job_id = str(uuid4())[-10:]
    print(job_id)
    prompt = body.build_prompt(job_id)
    job: Job | None = await queue.enqueue_job("generate", prompt=prompt, _job_id=job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Job creation failed")
    return TaskResponse(trigger_id=job_id, status=JobStatus.queued, trigger_type=TriggerType.generate)
