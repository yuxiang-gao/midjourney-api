from discord import Intents, Message
from discord.ext import commands
from loguru import logger

from app.settings import settings

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="", intents=intents)


@bot.event
async def on_ready():
    logger.success(f"Logged in as {bot.user} (ID: {bot.user.id})")


if __name__ == "__main__":
    bot.run(settings.bot_token)
