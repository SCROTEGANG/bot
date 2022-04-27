import logging

import discord
from discord.ext import commands

log = logging.getLogger(__name__)
pacts = (
    "pacts.pronoun",
    "pacts.tags",
    "pacts.scrote",
    "pacts.meta",
)


class DILF(commands.Bot):
    """DILF, the revolutionary Discord bot, made specifically for SCROTEGANG."""

    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            intents=discord.Intents.all()
        )

    async def setup_hook(self) -> None:
        for pact in pacts:
            try:
                await self.load_extension(pact)
            except commands.ExtensionError as e:
                log.error(f"error loading extension: {e}")

    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return

        await self.process_commands(msg)
