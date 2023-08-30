import asyncio
import random
from collections import defaultdict
from contextlib import asynccontextmanager
from typing import Any
from uuid import uuid4

from arq.connections import ArqRedis, create_pool
from arq.jobs import Job, JobStatus
from fastapi import APIRouter, Body, FastAPI, HTTPException, Query, Security, status
from loguru import logger

from app.api.models import TaskId, TaskInfo, TaskStatus
from app.discord.enums import TaskType
from app.settings import settings
from app.tasks.worker import redis_settings

from .models import *

context: Any = {"redis": None, "tasks": {}}


@asynccontextmanager
async def lifespan(app: FastAPI):
    context["redis"] = await create_pool(redis_settings)
    context["tasks"] = defaultdict(TaskStatus)
    logger.info(f"ARQ pool created: {context['redis']}")
    yield

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
    return TaskResponse(task_id=job_id, status=JobStatus.queued, task_type=TaskType.generate)


@router.get("/task/{task_id}")
async def get_task_status(task_id: str) -> TaskInfo:
    """Get the task status given the task id

    Args:
        task_id (str): task id

    Returns:
        TaskResult
    """
    # queue: ArqRedis = context["redis"]
    # job: Job = Job(task_id, queue, _deserializer=queue.job_deserializer)
    # res = await job.result_info()
    # logger.debug(f"Job {task_id} result: {res}")
    # if res is None:
    #     status: JobStatus = await job.status()
    #     logger.debug(f"Job {task_id} status: {status}")
    #     return TaskResponse(task_id=task_id, status=status)

    # return TaskResponse(
    #     task_id=task_id,
    #     status=JobStatus.complete,
    #     # result=res.result,
    # )

    queue: ArqRedis = context["redis"]
    job = await queue.enqueue_job("get_msgs", task_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Job creation failed")
    res = await job.result()
    logger.debug(res)
    return res
