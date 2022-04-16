from datetime import datetime, timezone

from discord.ext import commands
import discord

from .utils.db import EgoraptorTimestamp
from .utils._utils import delta_to_human

EGO_NAMES = ["egoraptor", "arin", "arin hanson"]
EGO_THINGS = ["pussy", "cunnilingus"]
IMAGES = {
    "ego": "egopussy.png"
}
IMAGES_BASE = "https://holedaemon.net/images/"

SCROTE_ID = 151516182439133184
TEST_ID = 779875531712757800


class Scrote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, m: discord.Message):
        if m.author.bot:
            return

        if m.guild.id != SCROTE_ID and m.guild.id != TEST_ID:
            return

        check = any(s in m.content.lower() for s in EGO_NAMES) and any(s in m.content.lower() for s in EGO_THINGS)
        if check:
            timestamp, exists = await EgoraptorTimestamp.get_or_create(defaults={
                "last_timestamp": datetime.utcnow()
            }, guild_id=str(m.guild.id))

            delta = datetime.now(timezone.utc) - timestamp.last_timestamp

            await m.reply(
                f"It has been {delta_to_human(delta)} since the last mention of egoraptor eating pussy"
                + "\n\n" + IMAGES_BASE + IMAGES["ego"]
            )


def setup(bot):
    bot.add_cog(Scrote(bot))
