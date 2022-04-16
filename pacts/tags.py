import logging

from tortoise import exceptions
from discord.ext import commands

from .utils.db import Tag

log = logging.getLogger(__name__)


class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, err):
        log.error(f"error during command: {err}")

        if isinstance(err.original, exceptions.IntegrityError):
            return await ctx.reply("A database error has occurred.")

    @commands.group(aliases=["tag"])
    async def tags(self, ctx: commands.Context):
        if not ctx.invoked_subcommand:
            return

    @tags.command(aliases=["create"])
    async def add(self, ctx: commands.Context, name: str, *, content: str):
        if content == "":
            return await ctx.reply("Tag content cannot be blank")

        exists = await Tag.exists(guild_id=str(ctx.guild.id), tag_name=name)
        if exists:
            return await ctx.reply("A tag by that name already exists")

        await Tag.create(
            guild_id=str(ctx.guild.id),
            author_id=str(ctx.author.id),
            tag_name=name,
            content=content,
        )

        await ctx.reply("Tag has been created")

    @tags.command()
    async def get(self, ctx: commands.Context, name: str):
        tag = await Tag.get_or_none(guild_id=str(ctx.guild.id), tag_name=name)
        if tag is None:
            return await ctx.reply("A tag by that name does not exist")

        await ctx.reply(tag.content)

    @tags.command()
    async def remove(self, ctx: commands.Context, name: str):
        tag = await Tag.get_or_none(guild_id=str(ctx.guild.id), tag_name=name)
        if tag is None:
            return await ctx.reply("A tag by that name does not exist.")

        perms = ctx.channel.permissions_for(ctx.author)
        if perms.manage_guild or tag.author_id is ctx.author.id:
            await tag.delete()
            return await ctx.reply("Tag has been deleted.")
        else:
            return await ctx.reply("You lack the rights to remove that tag")

    @tags.command()
    async def edit(self, ctx: commands.Context, name: str, *, new_content: str):
        if new_content == "":
            return await ctx.reply("Your new content cannot be blank")

        tag = await Tag.get_or_none(guild_id=str(ctx.guild.id), tag_name=name)
        if tag is None:
            return await ctx.reply("No tag by that name exists")

        perms = ctx.channel.permissions_for(ctx.author)
        if perms.manage_guild or tag.author_id is ctx.author.id:
            tag.content = new_content
            await tag.save()
            return await ctx.reply("Tag has been updated")
        else:
            return await ctx.reply("You lack the rights to edit that tag")

    @tags.command()
    async def rename(self, ctx: commands.Context, name: str, new_name: str):
        if new_name == "":
            return await ctx.reply("Your new content cannot be blank")

        tag = await Tag.get_or_none(guild_id=str(ctx.guild.id), tag_name=name)
        if tag is None:
            return await ctx.reply("No tag by that name exists")

        perms = ctx.channel.permissions_for(ctx.author)
        if perms.manage_guild or tag.author_id is ctx.author.id:
            tag.tag_name = new_name
            await tag.save()
            return await ctx.reply("Tag has been updated")
        else:
            return await ctx.reply("You lack the rights to rename that tag")


async def setup(bot):
    await bot.add_cog(Tags(bot))
