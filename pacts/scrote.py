from discord.ext import commands
import discord

EGO_NAMES = ["egoraptor", "arin", "arin hanson"]
EGO_THINGS = ["pussy", "cunnilingus"]
IMAGES = {
    "ego": "egopussy.png"
}

IMAGES_BASE = "https://holedaemon.net/images/"


class Scrote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, m: discord.Message):
        check = any(s in m.content.lower() for s in EGO_NAMES) and any(s in m.content.lower() for s in EGO_THINGS)
        if check:
            await m.reply(IMAGES_BASE + IMAGES["ego"])


def setup(bot):
    bot.add_cog(Scrote(bot))
