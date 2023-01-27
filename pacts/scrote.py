from __future__ import annotations
from typing import TYPE_CHECKING

from io import BytesIO
from datetime import datetime, timezone

from discord.ext import commands
import discord

from .utils.db import EgoraptorTimestamp
from .utils._utils import delta_to_human

if TYPE_CHECKING:
    from bot import DILF


EGO_NAMES = ["egoraptor", "arin", "arin hanson"]
EGO_THINGS = ["pussy", "cunnilingus", "vagina", "cunt"]
IMAGE = "https://holedaemon.net/images/egopussy.png"
VALID_GUILDS = [
    # SCROTEGANG
    151516182439133184,
    # Testing
    779875531712757800
]


class Scrote(commands.Cog):
    """Unfortunate functionality specific to SCROTEGANG."""

    def __init__(self, bot: DILF):
        self.bot: DILF = bot
        self.image = None

    @commands.Cog.listener()
    async def on_message(self, m: discord.Message):
        if m.author.bot:
            return

        if m.guild.id not in VALID_GUILDS:
            return

        check = any(s in m.content.lower() for s in EGO_NAMES) and any(s in m.content.lower() for s in EGO_THINGS)
        if check:
            timestamp, exists = await EgoraptorTimestamp.get_or_create(defaults={
                "last_timestamp": datetime.utcnow()
            }, guild_id=str(m.guild.id))

            delta = datetime.now(timezone.utc) - timestamp.last_timestamp

            if self.image is None:
                async with self.bot.session.get(IMAGE) as resp:
                    self.image = await resp.read()

            file = discord.File(
                BytesIO(self.image),
                "egopussy.png",
                spoiler=False,
                description="A sign from Spongebob Squarepants labeled \"0 days since last mention of egoraptor eating pussy\"",  # noqa: E501
            )
            await m.reply(
                f"It has been {delta_to_human(delta)} since the last mention of egoraptor eating pussy",
                file=file,
            )

            timestamp.update_from_dict({
                "last_timestamp": datetime.utcnow(),
            })
            await timestamp.save()


async def setup(bot: DILF):
    await bot.add_cog(Scrote(bot))
