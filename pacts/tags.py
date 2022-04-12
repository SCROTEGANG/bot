from discord.ext import commands


class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _get_tag(self, ctx: commands.Context, name: str):
        tag = await self.bot.conn.fetchrow(
            """SELECT * FROM tags WHERE tag_name = $1 AND guild_id = $2;""",
            name.lower(),
            str(ctx.guild.id),
        )
        return tag

    @commands.group(aliases=["tag"])
    async def tags(self, ctx: commands.Context):
        if not ctx.invoked_subcommand:
            if ctx.subcommand_passed is not None:
                tag = await self._get_tag(ctx, ctx.subcommand_passed)
                if tag is not None:
                    await ctx.reply(tag["content"])

    @tags.command()
    async def add(self, ctx: commands.Context, name: str, *, content: str):
        if content == "":
            return await ctx.reply("Tag content cannot be blank")

        tag = await self._get_tag(ctx, name)
        if tag is not None:
            return await ctx.reply("A tag by that name already exists")

        await self.bot.conn.execute(
            "INSERT INTO tags (guild_id, author_id, tag_name, content) VALUES ($1, $2, $3, $4);",
            str(ctx.guild.id),
            str(ctx.author.id),
            name.lower(),
            content,
        )

        await ctx.reply("Tag has been created")

    @tags.command()
    async def get(self, ctx: commands.Context, name: str):
        tag = await self._get_tag(ctx, name)
        if tag is None:
            return await ctx.reply("A tag by that name does not exist")

        await ctx.reply(tag["content"])

    @tags.command()
    async def remove(self, ctx: commands.Context, name: str):
        tag = await self._get_tag(ctx, name)
        if tag is None:
            return await ctx.reply("A tag by that name does not exist.")

        perms = ctx.channel.permissions_for(ctx.author)
        if perms.manage_guild or tag["author_id"] is ctx.author.id:
            await self.bot.conn.execute(
                "DELETE FROM tags WHERE tag_name = $1 AND guild_id = $2",
                name,
                str(ctx.guild.id),
            )
            return await ctx.reply("Tag has been deleted.")
        else:
            return await ctx.reply("You lack the rights to remove that tag")

    @tags.command()
    async def edit(self, ctx: commands.Context, name: str, *, new_content: str):
        if new_content == "":
            return await ctx.reply("Your new content cannot be blank")

        tag = await self._get_tag(ctx, name)
        if tag is None:
            return await ctx.reply("No tag by that name exists")

        perms = ctx.channel.permissions_for(ctx.author)
        if perms.manage_guild or tag["author_id"] is ctx.author.id:
            await self.bot.conn.execute(
                "UPDATE tags SET content = $1 WHERE tag_name = $2 AND guild_id = $3",
                new_content,
                name,
                ctx.guild.id,
                )
            return await ctx.reply("Tag has been updated")
        else:
            return await ctx.reply("You lack the rights to edit that tag")

    @tags.command()
    async def rename(self, ctx: commands.Context, name: str, new_name: str):
        tag = await self._get_tag(ctx, name)
        if tag is None:
            return await ctx.reply("No tag by that name exists")

        perms = ctx.channel.permissions_for(ctx.author)
        if perms.manage_guild or tag["author_id"] is ctx.author.id:
            await self.bot.conn.execute(
                "UPDATE tags SET tag_name = $1 WHERE tag_name = $2 AND guild_id = $3;",
                new_name.lower(),
                name.lower(),
                str(ctx.guild.id),
            )
            return await ctx.reply("Tag has been renamed")
        else:
            return await ctx.reply("You lack the rights to rename that tag")


def setup(bot):
    bot.add_cog(Tags(bot))
