import asyncio
import functools
from typing import Any, Dict

import httpx
from arq import Retry
from arq.jobs import Job
from loguru import logger

from app.settings import settings


def make_payload(trigger_type: int, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    payload = {
        "type": trigger_type,
        "application_id": "936929561302675456",
        "guild_id": settings.guild_id,
        "channel_id": settings.channel_id,
        "session_id": "cb06f61453064c0983f2adae2a88c223",
        "data": data,
    }
    payload.update(kwargs)
    return payload


async def startup(ctx: dict) -> None:
    logger.info("ARQ: Starting up")
    ctx["httpx_client"] = httpx.AsyncClient(
        base_url=settings.discord_base_url,
        headers={"Content-Type": "application/json", "Authorization": settings.user_token},
    )


async def shutdown(ctx: dict) -> None:
    logger.info("ARQ: Shutting down")
    await ctx["httpx_client"].aclose()


async def generate(ctx: dict, prompt: str) -> bool:
    logger.info(f"ARQ: generate: {prompt}")
    payload = make_payload(
        2,
        {
            "version": "1118961510123847772",
            "id": "938956540159881230",
            "name": "imagine",
            "type": 1,
            "options": [{"type": 3, "name": "prompt", "value": prompt}],
            "attachments": [],
        },
    )

    client: httpx.AsyncClient = ctx["httpx_client"]
    try:
        resp = await client.post("/interactions", json=payload)
        resp.raise_for_status()
    except httpx.HTTPStatusError as e:
        logger.error(f"ARQ: generate: {e}")
        logger.error(f"Exception in generate: {e}, retrying in {settings.retry_defer} seconds")
        raise Retry(defer=settings.retry_defer)
    return resp.is_success
