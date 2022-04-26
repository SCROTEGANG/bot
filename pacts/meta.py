import datetime

from discord.ext import commands
import discord


class Meta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_change = None

    @commands.command()
    async def game(self, ctx: commands.Context, *, new_game: str):
        if self.last_change is not None:
            last = datetime.datetime.now() - self.last_change
            then = self.last_change + datetime.timedelta(hours=1)

            if last.total_seconds() < 3600:
                return await ctx.reply(
                    f"The game can only be changed once per hour. Wait until <t:{int(then.timestamp())}>"
                )

        game = discord.Game(new_game)
        await self.bot.change_presence(activity=game)
        await ctx.reply("Game has been changed")
        self.last_change = datetime.datetime.now()


async def setup(bot):
    await bot.add_cog(Meta(bot))
