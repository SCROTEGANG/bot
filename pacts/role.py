from typing import Optional

import discord
from discord.ext import commands

from ._utils import PRONOUN_RE


class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_role(self, ctx: commands.Context) -> Optional[discord.Role]:
        if len(ctx.author.roles) == 1:
            return None

        role = ctx.author.roles[len(ctx.author.roles)-1]
        if not PRONOUN_RE.match(role.name):
            return role
        else:
            return None

    @commands.group()
    async def role(self, ctx: commands.Context):
        if not ctx.invoked_subcommand:
            return

    @role.command()
    @commands.bot_has_permissions(manage_roles=True)
    async def rename(self, ctx: commands.Context, *, name: str):
        role = self.get_role(ctx)
        if role is None:
            return await ctx.reply("Cannot find role")

        await role.edit(name=name, reason="Command requested")
        return await ctx.reply(f"Your role's been changed to `{name}`, for some reason....")

    @role.command()
    @commands.bot_has_permissions(manage_roles=True)
    async def paint(self, ctx: commands.Context, hex: str):
        role = self.get_role(ctx)
        if role is None:
            return await ctx.reply("Cannot find role")

        if hex.startswith("#"):
            hex = hex[1:]

        color = int(hex, 16)

        await role.edit(color=color)
        return await ctx.reply("Color has been changed, numbnuts")


def setup(bot):
    bot.add_cog(Role(bot))
