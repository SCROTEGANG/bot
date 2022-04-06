import logging

import discord
import asyncpg
from discord.ext import commands

log = logging.getLogger(__name__)
pacts = (
    "pacts.pronoun",
    # "pacts.role"
)


class SCROTUS(commands.Bot):
    conn: asyncpg.Connection
    opts: dict

    def __init__(self, opts: dict, conn: asyncpg.Connection):
        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            description="A very specialized general-purpose bot for SCROTEGANG",
        )

        self.conn = conn
        self.opts = opts

        for pact in pacts:
            try:
                self.load_extension(pact)
            except commands.ExtensionError as e:
                log.error(f"error loading extension: {e}")

    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return

        await self.process_commands(msg)
