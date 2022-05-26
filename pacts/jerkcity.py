from __future__ import annotations
from typing import TYPE_CHECKING, Any, Dict, List
from urllib.parse import quote_plus
from itertools import islice
import datetime
import logging

from discord.ext import commands
import discord

if TYPE_CHECKING:
    from bot import DILF

log = logging.getLogger(__name__)
JERKCITY_ROOT_URL = "https://bonequest.com/api/v2"
USER_AGENT = "DILF"

PANTS_EMOJI = "<:pants:796846070314565652>"


class JerkcityException(Exception):
    def __init__(self, code: int):
        self.code = code


class JerkcityEpisode:
    def __init__(self, data: Dict[str, Any]):
        self.title: str = data.get("title")
        self.day: int = data.get("day")
        self.dialog: List[List[str]] = data.get("dialog")
        self.episode: int = data.get("episode")
        self.height: int = data.get("height")
        self.image: str = data.get("image")
        self.month: int = data.get("month")
        self.navigation: Dict[JerkcityEpisode] = data.get("navigation")
        self.players: List[str] = data.get("players")
        self.tags: List[str] = data.get("tags")
        self.thumb: str = data.get("thumb")
        self.width: int = data.get("width")
        self.year: int = data.get("year")

    def to_embed(self) -> discord.Embed:
        dt = datetime.datetime(year=self.year, month=self.month, day=self.day)

        e = discord.Embed(
            title=f"{self.title}",
            color=discord.Color.dark_blue(),
            timestamp=dt,
            url=f"https://bonequest.com/{self.episode}"
        )
        e.set_image(url=f"https://bonequest.com/{self.image}")
        return e


class Jerkcity(commands.Cog):
    """Commands for interacting with Jerkcity/Bonequest."""

    def __init__(self, bot: DILF):
        self.bot: DILF = bot

    async def request(self, uri: str) -> Any:
        headers = {
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        }

        url = f'{JERKCITY_ROOT_URL}/{uri}'
        async with self.bot.session.get(url, headers=headers) as resp:
            if resp.status != 200:
                raise JerkcityException(resp.status)
            else:
                return await resp.json()

    async def get_random(self, ctx: commands.Context) -> None:
        try:
            resp = await self.request("episodes/random/1")
            episodes = resp.get("episodes")
            episode = JerkcityEpisode(episodes[0])

            if episode is None:
                await ctx.reply(f"{PANTS_EMOJI} <(HLAGHGLAHLGHALGHLAGHJALGH)")
                return

            await ctx.reply(embed=episode.to_embed())
        except JerkcityException as e:
            log.error(f"jerkcity returned status code {e.code}")
            await ctx.reply(f"{PANTS_EMOJI} <(SOMETHING BROKE)")

    @commands.group(aliases=["jc", "bq", "bonequest"])
    async def jerkcity(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await self.get_random(ctx)

    @jerkcity.command(aliases=["episode"])
    async def comic(self, ctx: commands.Context, episode: int):
        try:
            resp = await self.request(f"episodes/{episode}")
            episodes = resp.get("episodes")
            ep = JerkcityEpisode(episodes[0])

            if ep is None:
                return await ctx.reply(f"{PANTS_EMOJI} <(HLAGHGLAHLGHALGHLAGHJALGH)")

            return await ctx.reply(embed=ep.to_embed())
        except JerkcityException as e:
            log.error(f"jerkcity returned status code {e.code}")
            await ctx.reply(f"{PANTS_EMOJI} <(SOMETHING BROKE)")

    @jerkcity.command()
    async def random(self, ctx: commands.Context):
        await self.get_random(ctx)

    @jerkcity.command()
    async def search(self, ctx: commands.Context, *, query: str):
        try:
            resp = await self.request(f"search/?q={quote_plus(query)}")
            episodes: List[Dict] = resp.get("episodes")
            if episodes is None or len(episodes) == 0:
                return await ctx.reply(f"{PANTS_EMOJI} <(NOTHING)")

            each = {}
            for x in islice(episodes, 9):
                each[x.get("episode")] = x.get("title")

            each_sorted = [f"[{k} - {each[k]}](https://bonequest.com/{k})" for k in sorted(each.keys())]

            desc = "\n".join(each_sorted)
            if len(episodes) > 10:
                desc += f"\n[{len(episodes)-10} more](https://bonequest.com/search/?q={quote_plus(query)})"

            e = discord.Embed(color=discord.Color.dark_blue(), description=desc)
            await ctx.reply(embed=e)
        except JerkcityException as e:
            log.error(f"jerkcity returned status code {e.code}")
            await ctx.reply(f"{PANTS_EMOJI} <(UH OH)")


async def setup(bot: DILF):
    await bot.add_cog(Jerkcity(bot))
