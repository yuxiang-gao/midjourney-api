import asyncio
import re
from collections import defaultdict

import discord
from discord import Client, Intents, Message
from discord.ext import commands
from loguru import logger

from midjourney_api.api.models import TaskId, TaskInfo, TaskStatus
from midjourney_api.settings import settings


class DiscordClient(Client):
    msgs: defaultdict = defaultdict(lambda: None)

    async def on_ready(self):
        logger.success(f"Logged in as {bot.user} (ID: {bot.user.id})")
        logger.info(bot)

    async def on_message(self, message: Message):
        if message.author.id != settings.mj_bot_id:
            return

        task_id = TaskId.from_prompt(message.content)
        if not task_id:
            return

        logger.debug(f"on_message: {message.content}")
        logger.debug(f"on_message embeds: {message.embeds[0].to_dict() if message.embeds else message.embeds}")

        # logger.debug(f"on_message embeds: {[r for r in message.components]}")
        logger.debug([[c.custom_id for c in r.children] for r in message.components])

        def flatten(l):
            return [item for sublist in l for item in sublist]

        actions = flatten([[c.custom_id for c in r.children] for r in message.components])
        attachements = [a.url for a in message.attachments]

        status = None
        if message.content.find("Waiting to start") != -1:
            status = TaskStatus.waiting
        elif message.content.find("(Stopped)") != -1:
            status = TaskStatus.failed
        else:
            status = TaskStatus.finished
        # from rich import inspect

        # inspect(message)

        if self.msgs[task_id.id] is None or status == TaskStatus.waiting:
            self.msgs[task_id.id] = TaskInfo(
                id=task_id.id,
                status=status,
                actions=actions,
                attachments=attachements,
                created_at=message.created_at,
                progress=0,
            )
        else:
            self.msgs[task_id.id].status = status
            self.msgs[task_id.id].actions = actions
            self.msgs[task_id.id].finished_at = message.created_at

    async def on_message_edit(self, _: Message, after: Message):
        if after.author.id != 936929561302675456:
            return
        task_id = TaskId.from_prompt(after.content)
        if not task_id:
            return

        match = re.search(r"\((\d+)%\)", after.content)
        progress = 0.0
        if match:
            progress = float(match.group(1)) / 100.0

        if self.msgs[task_id.id] is not None:
            self.msgs[task_id.id].progress = progress
            self.msgs[task_id.id].status = TaskStatus.running

        logger.debug(f"on_message_edit: {after.content}---{progress}")


def make_bot():
    intents = discord.Intents.default()
    intents.message_content = True

    return DiscordClient(intents=intents)


if __name__ == "__main__":
    make_bot().run(settings.bot_token)
