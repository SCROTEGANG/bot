import logging

import asyncpg
import discord
from discord.ext import commands

log = logging.getLogger(__name__)
pacts = (
    "pacts.pronoun",
    "pacts.tags",
    "pacts.scrote",
)


class SCROTUS(commands.Bot):
    def __init__(self, conn: asyncpg.Connection):
        super().__init__(command_prefix=commands.when_mentioned_or("!"))

        self.conn = conn

        for pact in pacts:
            try:
                self.load_extension(pact)
            except commands.ExtensionError as e:
                log.error(f"error loading extension: {e}")

    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return

        await self.process_commands(msg)
