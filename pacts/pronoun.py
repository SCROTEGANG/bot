import discord
from discord.ext import commands

from .utils._utils import PRONOUNS, PRONOUN_RE


class Pronoun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=["pronouns"])
    async def pronoun(self, ctx: commands.Context):
        if not ctx.invoked_subcommand:
            return

    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    @pronoun.command()
    async def init(self, ctx: commands.Context):
        g: discord.Guild = self.bot.get_guild(ctx.guild.id)
        existing = len([r for r in g.roles if r.name in PRONOUNS])
        created = 0

        not_needed = []
        for r in PRONOUNS:
            for gr in g.roles:
                if r == gr.name:
                    not_needed.append(r)

        roles = [r for r in PRONOUNS if r not in not_needed]
        for r in roles:
            await g.create_role(name=r)
            created += 1

        return await ctx.reply(f"Initialized pronoun roles; {existing} existing; {created} created")

    @commands.bot_has_permissions(manage_roles=True)
    @pronoun.command()
    async def add(self, ctx: commands.Context, role: discord.Role):
        if not PRONOUN_RE.match(role.name):
            return

        await ctx.author.add_roles(role)
        return await ctx.reply(f"You now have the `{role.name}` role")

    @commands.bot_has_permissions(manage_roles=True)
    @pronoun.command()
    async def remove(self, ctx: commands.Context, role: discord.Role):
        if not PRONOUN_RE.match(role.name):
            return

        await ctx.author.remove_roles(role)
        return await ctx.reply(f"You no longer have the `{role.name}` role")

    @pronoun.command()
    async def list(self, ctx: commands.Context):
        g = self.bot.get_guild(ctx.guild.id)
        roles = [r for r in g.roles if PRONOUN_RE.match(r.name)]

        prns = ""
        if len(roles) > 0:
            for r in roles:
                prns += f"{r.name}, "
            prns = prns[:-2]
        else:
            prns = "none"

        return await ctx.reply(f"Pronouns: {prns}")


def setup(bot):
    bot.add_cog(Pronoun(bot))
