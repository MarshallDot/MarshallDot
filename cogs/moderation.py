import asyncio
import logging

import aiohttp
import discord
from discord.ext import commands

import enchant

bott: commands.Bot


def check(ctx):
    for i in enchant.Shell.servers():
        if int(i) == ctx.guild.id:
            return True
    return False


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bott = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    @commands.check(check)
    async def post(self, ctx: commands.Context, channel: discord.TextChannel, *, message):
        await ctx.message.delete()
        await channel.send(message)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    @commands.check(check)
    async def clear(self, ctx: commands.Context, amount=5):
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send("```"
                       f"{len(deleted)} message deleted!"
                       "```", delete_after=4)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    @commands.check(check)
    async def ban(self, ctx: commands.Context, member: discord.Member, reason=None):
        await ctx.message.delete()
        if not reason:
            await member.ban()
        else:
            await member.ban(reason=reason)
        headers = {
            'User-Agent': f'{ctx.guild.id} ban_message'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:6006/', headers=headers) as r:
                if r.status == 200:
                    js = await r.json()
                    data = js[0]["data"]
        if data == "None":
            await ctx.send("```"
                           f"{member} got bent!"
                           "```")
        else:
            headers = {
                'User-Agent': f'{ctx.guild.id} ban_message'
            }
            async with aiohttp.ClientSession() as session:
                async with session.get('http://localhost:6006/', headers=headers) as r:
                    if r.status == 200:
                        js = await r.json()
                        data = js[0]["data"]
            pos = data.split(" ")
            text = ""
            for i in pos:
                if i == "{member}":
                    text += f"{member} "
                else:
                    text += f"{i} "
            await ctx.send(text)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.guild_only()
    @commands.check(check)
    async def kick(self, ctx: commands.Context, member: discord.Member, reason=None):
        await ctx.message.delete()
        if not reason:
            await member.kick()
        else:
            await member.kick(reason=reason)
        headers = {
            'User-Agent': f'{ctx.guild.id} kick_message'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:6006/', headers=headers) as r:
                if r.status == 200:
                    js = await r.json()
                    data = js[0]["data"]
        if data == "None":
            await ctx.send("```"
                           f"{member} kicked"
                           "```")
        else:
            headers = {
                'User-Agent': f'{ctx.guild.id} kick_message'
            }
            async with aiohttp.ClientSession() as session:
                async with session.get('http://localhost:6006/', headers=headers) as r:
                    if r.status == 200:
                        js = await r.json()
                        data = js[0]["data"]
            pos = data.split(" ")
            text = ""
            for i in pos:
                if i == "{member}":
                    text += f"{member} "
                else:
                    text += f"{i} "
            await ctx.send(text)

    @commands.command(name="force-ban")
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    @commands.check(check)
    async def force(self, ctx: commands.Context, id):
        try:
            forced = enchant.enchants.r.get(f"{ctx.guild.id}_forced")
        except:
            enchant.enchants.r.set(f"{ctx.guild.id}_forced", id)
            return
        forcedd = str(forced) + f", {id}"
        enchant.enchants.r.set(f"{ctx.guild.id}_forced", forcedd)
        headers = {
            'User-Agent': f'{ctx.guild.id} forc_ban_message'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:6006/', headers=headers) as r:
                if r.status == 200:
                    js = await r.json()
                    data = js[0]["data"]
        if data == "None":
            await ctx.reply("```"
                            f"{id} force banned"
                            "```")
        else:
            headers = {
                'User-Agent': f'{ctx.guild.id} force_ban_message'
            }
            async with aiohttp.ClientSession() as session:
                async with session.get('http://localhost:6006/', headers=headers) as r:
                    if r.status == 200:
                        js = await r.json()
                        data = js[0]["data"]
            pos = data.get("force_ban_message").split(" ")
            text = ""
            for i in pos:
                if i == "{member}":
                    text += f"{id} "
                else:
                    text += f"{i} "
            await ctx.reply(text)

    @commands.command(name="temp-ban")
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    @commands.check(check)
    async def temp(self, ctx: commands.Context, member: discord.Member, time="24h", reason=None):
        await ctx.message.delete()
        if not reason:
            await member.ban()
        else:
            await member.ban(reason=reason)
        headers = {
            'User-Agent': f'{ctx.guild.id} temp_ban_message'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:6006/', headers=headers) as r:
                if r.status == 200:
                    js = await r.json()
                    data = js[0]["data"]
        if data == "None":
            await ctx.send("```"
                           f"{member} got bent for a while"
                           "```")
        else:
            headers = {
                'User-Agent': f'{ctx.guild.id} temp_ban_message'
            }
            async with aiohttp.ClientSession() as session:
                async with session.get('http://localhost:6006/', headers=headers) as r:
                    if r.status == 200:
                        js = await r.json()
                        data = js[0]["data"]
            pos = data.split(" ")
            text = ""
            for i in pos:
                if i == "{member}":
                    text += f"{member} "
                else:
                    text += f"{i} "
            await ctx.send(text)
        if time.endswith("h"):
            pos = time.split("h")
            time = int(pos[0]) * 3600
            await asyncio.sleep(time)
            await member.unban()
        elif time.endswith("m"):
            pos = time.split("m")
            time = int(pos[0]) * 60
            await asyncio.sleep(time)
            await member.unban()
        elif time.endswith("s"):
            pos = time.split("s")
            time = int(pos[0])
            await asyncio.sleep(time)
            await member.unban()
        else:
            await ctx.send("The given time type is invalid eg: 1h (hours(s))")


def setup(bot: commands.Bot):
    log = logging.getLogger("shmoke")
    log.log(4242, "Moderation loaded")
    bot.add_cog(Moderation(bot))
