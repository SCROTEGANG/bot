import re

import discord
from discord.ext import commands

from ._utils import PRONOUNS

PRONOUN_RE = re.compile(r"\w+\/\w+")


class Pronouns(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def pronouns(self, ctx: commands.Context):
        if not ctx.invoked_subcommand:
            return

    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    @pronouns.command()
    async def init(self, ctx: commands.Context):
        g: discord.Guild = self.bot.get_guild(ctx.guild.id)
        existing = len([r for r in g.roles if r.name in PRONOUNS])
        created = 0

        roles = []
        for r in g.roles:
            if r.name not in PRONOUNS and PRONOUN_RE.match(r.name):
                roles.append(r.name.lower())

        for r in roles:
            await g.create_role(name=r)
            created += 1

        await ctx.reply(f"Initialized pronoun roles; {existing} existing; {created} created")

    @commands.bot_has_permissions(manage_roles=True)
    @pronouns.command()
    async def add(self, ctx: commands.Context, role: discord.Role):
        if not PRONOUN_RE.match(role.name):
            return

        await ctx.author.add_roles(role)
        return await ctx.reply(f"Thou hath been branded `{role.name}`")

    @commands.bot_has_permissions(manage_roles=True)
    @pronouns.command()
    async def remove(self, ctx: commands.Context, role: discord.Role):
        if not PRONOUN_RE.match(role.name):
            return

        await ctx.author.remove_roles(role)
        return await ctx.reply(f"Thou no longer bears the brand of `{role.name}`")


def setup(bot):
    bot.add_cog(Pronouns(bot))
