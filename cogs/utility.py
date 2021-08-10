import logging

import aiohttp
import discord
from discord.ext import commands

import enchant
import network

bott: commands.Bot


def check(ctx):
    for i in enchant.Shell.servers():
        if int(i) == ctx.guild.id:
            return True
    return False


class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bott = bot

    @commands.command(name="log")
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    @commands.check(check)
    async def logs(self, ctx: commands.Context, id):
        log = enchant.get_log(str(id), ctx.guild.id)
        await ctx.reply("```"
                        f"{log}"
                        "```")

    @commands.command(name="upload")
    @commands.check(check)
    async def ulo(self, ctx: commands.Context, url=None):
        id = self.bot.apid()
        if not url:
            attachment_url: str = ctx.message.attachments[0].url
            urlpos = attachment_url.split("https://cdn.discordapp.com/attachments/")
            enchant.upload(id, urlpos[1])
        else:
            attachment_url: str = url
            if attachment_url.startswith("https://discord.com/channels/"):
                urlpos = attachment_url.split("https://discord.com/channels/")
            elif attachment_url.startswith("https://cdn.discordapp.com/attachments/"):
                urlpos = attachment_url.split("https://cdn.discordapp.com/attachments/")
            enchant.upload(id, urlpos[1])
        await ctx.reply("```"
                        f"You attachment id: {id}"
                        "```")

    @commands.command(name="download")
    @commands.check(check)
    async def lo(self, ctx: commands.Context, pid):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://cdn.tortiy.tk/{pid}') as r:
                if r.status == 404:
                    jso = await r.json()
                    await ctx.reply(f'```{jso["message"]}```')
                    return
                if r.status == 400:
                    jso = await r.json()
        url = f"https://cdn.tortiy.tk/{pid}"
        await ctx.reply(f"{url}")

    @commands.command(name="get-message-log")
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.check(check)
    async def _getmessage(self, ctx: commands.Context):
        headers = {
            'User-Agent': f'{ctx.guild.id} message_log'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:6006/', headers=headers) as r:
                if r.status == 200:
                    js = await r.json()
                    data = js[0]["data"]
        prefix = enchant.get_prefix()
        if data:
            await ctx.author.send(
                file=discord.File(f'../data/{ctx.guild.id}_messages.txt'))
        else:
            await ctx.reply("```"
                            "Message logging is not enabled for your server.\n"
                            f'If you want to enable message logging for your server: '
                            f'"{prefix}configuration all message-log on"'
                            "```")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.check(check)
    async def note(self, ctx: commands.Context, member: discord.Member, *, note=None):
        if not note:
            try:
                nt = network.database.r.get(f"{ctx.guild.id}_{member.id}_note")
            except:
                await ctx.reply("```"
                                f"No notes about this user"
                                "```")
                return
            await ctx.reply("```"
                            f"Note about this user: {nt}"
                            "```")
        else:
            network.database.r.set(f"{ctx.guild.id}_{member.id}_note", note)
            await ctx.reply("```"
                            f"User's note changed"
                            "```")

    @commands.command(name="database")
    async def tag(self, ctx: commands.Context, name, *, value=None):
        if not value:
            try:
                nt = network.database.r.get(f"{ctx.guild.id}_{name}_tag")
            except:
                await ctx.reply("```"
                                f"No data about this name on database"
                                "```")
                return
            await ctx.reply(f"{nt.decode()}")
        else:
            network.database.r.set(f"{ctx.guild.id}_{name}_tag", value)
            await ctx.reply("```"
                            f"This value has been added to the database with its name."
                            "```")


def setup(bot: commands.Bot):
    log = logging.getLogger("shmoke")
    log.log(4242, "Utility loaded")
    bot.add_cog(Utility(bot))
