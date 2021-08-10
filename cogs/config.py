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


class Config(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bott = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.check(check)
    async def setup(self, ctx: commands.Context, service, value=None):
        if service == "mod-log":
            headers = {
                'User-Agent': f'{ctx.guild.id} mod_log'
            }
            async with aiohttp.ClientSession() as session:
                async with session.get('http://localhost:6006/', headers=headers) as r:
                    if r.status == 200:
                        js = await r.json()
                        data = js[0]["data"]
            if not data:
                headers = {
                    'User-Agent': f'{ctx.guild.id} message_log'
                }
                async with aiohttp.ClientSession() as session:
                    async with session.get('http://localhost:6006/', headers=headers) as r:
                        if r.status == 200:
                            js = await r.json()
                            data = js[0]["data"]
                if not data:
                    await ctx.reply("```"
                                    "Before you can open mod-log you need to open Message-log."
                                    "```")
                if not value:
                    await ctx.reply("```"
                                    "Please specify a text channel"
                                    "```")
                    return
                value = value.split("<#")
                value = value[1].split(">")
                value = value[0]
                headers = {
                    'User-Agent': f'{ctx.guild.id} mod_log True'
                }
                async with aiohttp.ClientSession() as session:
                    async with session.put('http://localhost:6006/', headers=headers) as r:
                        if r.status == 200:
                            js = await r.json()
                            data = js[0]["data"]
                headers = {
                    'User-Agent': f'{ctx.guild.id} mod_log_channel {value}'
                }
                async with aiohttp.ClientSession() as session:
                    async with session.put('http://localhost:6006/', headers=headers) as r:
                        if r.status == 200:
                            js = await r.json()
                            data = js[0]["data"]
                await ctx.reply("```"
                                "Mod-log enabled"
                                "```")
            else:
                headers = {
                    'User-Agent': f'{ctx.guild.id} mod_log False'
                }
                async with aiohttp.ClientSession() as session:
                    async with session.put('http://localhost:6006/', headers=headers) as r:
                        if r.status == 200:
                            js = await r.json()
                            data = js[0]["data"]
                await ctx.reply("```"
                                "Mod-log disabled"
                                "```")
        elif service == "message-log":
            headers = {
                'User-Agent': f'{ctx.guild.id} message_log'
            }
            async with aiohttp.ClientSession() as session:
                async with session.get('http://localhost:6006/', headers=headers) as r:
                    if r.status == 200:
                        js = await r.json()
                        data = js[0]["data"]
            if not data:
                headers = {
                    'User-Agent': f'{ctx.guild.id} message_log True'
                }
                async with aiohttp.ClientSession() as session:
                    async with session.put('http://localhost:6006/', headers=headers) as r:
                        if r.status == 200:
                            js = await r.json()
                            data = js[0]["data"]
                await ctx.reply("```"
                                "Message-log enabled"
                                "```")
            else:
                headers = {
                    'User-Agent': f'{ctx.guild.id} message_log False'
                }
                async with aiohttp.ClientSession() as session:
                    async with session.put('http://localhost:6006/', headers=headers) as r:
                        if r.status == 200:
                            js = await r.json()
                            data = js[0]["data"]
                await ctx.reply("```"
                                "Message-log disabled"
                                "```")
        elif service == "spam-filter":
            headers = {
                'User-Agent': f'{ctx.guild.id} spam_filter'
            }
            async with aiohttp.ClientSession() as session:
                async with session.get('http://localhost:6006/', headers=headers) as r:
                    if r.status == 200:
                        js = await r.json()
                        data = js[0]["data"]
            if not data:
                headers = {
                    'User-Agent': f'{ctx.guild.id} spam_filter True'
                }
                async with aiohttp.ClientSession() as session:
                    async with session.put('http://localhost:6006/', headers=headers) as r:
                        if r.status == 200:
                            js = await r.json()
                            data = js[0]["data"]
                await ctx.reply("```"
                                "Spam-filter enabled"
                                "```")
            else:
                headers = {
                    'User-Agent': f'{ctx.guild.id} mod_log False'
                }
                async with aiohttp.ClientSession() as session:
                    async with session.put('http://localhost:6006/', headers=headers) as r:
                        if r.status == 200:
                            js = await r.json()
                            data = js[0]["data"]
                await ctx.reply("```"
                                "Spam-filter disabled"
                                "```")
        elif service == "profanity-filter":
            headers = {
                'User-Agent': f'{ctx.guild.id} profanity_filter'
            }
            async with aiohttp.ClientSession() as session:
                async with session.get('http://localhost:6006/', headers=headers) as r:
                    if r.status == 200:
                        js = await r.json()
                        data = js[0]["data"]
            if not data:
                headers = {
                    'User-Agent': f'{ctx.guild.id} profanity_filter True'
                }
                async with aiohttp.ClientSession() as session:
                    async with session.put('http://localhost:6006/', headers=headers) as r:
                        if r.status == 200:
                            js = await r.json()
                            data = js[0]["data"]
                await ctx.reply("```"
                                "Profanity-filter enabled"
                                "```")
            else:
                headers = {
                    'User-Agent': f'{ctx.guild.id} profanity_filter False'
                }
                async with aiohttp.ClientSession() as session:
                    async with session.put('http://localhost:6006/', headers=headers) as r:
                        if r.status == 200:
                            js = await r.json()
                            data = js[0]["data"]
                await ctx.reply("```"
                                "Profanity-filter disabled"
                                "```")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.check(check)
    async def configuration(self, ctx: commands.Context, command: str, typer: str, *, value):
        typer = typer.replace("-", "_")
        command = command.replace("-", "_")
        if value == "on":
            value = True
        elif value == "off":
            value = False
        if command == "all":
            if typer == "prefix":
                headers = {
                    'User-Agent': f'{ctx.guild.id} prefix {value}'
                }
                async with aiohttp.ClientSession() as session:
                    async with session.put('http://localhost:6006/', headers=headers) as r:
                        if r.status == 200:
                            js = await r.json()
                            data = js[0]["data"]
                await ctx.reply("```"
                                "Configurations applied"
                                "```")
            else:
                await ctx.reply("```"
                                "Unkown type"
                                "```")
        elif command == "ban":
            if typer == "message":
                if len(value) > 1000:
                    await ctx.reply("```"
                                    f"Ban message can be up to 1000 characters"
                                    "```")
                    return
                headers = {
                    'User-Agent': f'{ctx.guild.id} {command}_{typer} {value}'
                }
                async with aiohttp.ClientSession() as session:
                    async with session.put('http://localhost:6006/', headers=headers) as r:
                        if r.status == 200:
                            js = await r.json()
                            data = js[0]["data"]
                await ctx.reply("```"
                                "Configurations applied"
                                "```")
            else:
                await ctx.reply("```"
                                "Unkown type"
                                "```")
        elif command == "temp_ban":
            if typer == "message":
                if len(value) > 1000:
                    await ctx.reply("```"
                                    f"Temp-ban message can be up to 1000 characters"
                                    "```")
                    return
                headers = {
                    'User-Agent': f'{ctx.guild.id} {command}_{typer} {value}'
                }
                async with aiohttp.ClientSession() as session:
                    async with session.put('http://localhost:6006/', headers=headers) as r:
                        if r.status == 200:
                            js = await r.json()
                            data = js[0]["data"]
                await ctx.reply("```"
                                "Configurations applied"
                                "```")
            else:
                await ctx.reply("```"
                                "Unkown type"
                                "```")
        elif command == "kick":
            if typer == "message":
                if len(value) > 1000:
                    await ctx.reply("```"
                                    f"Kick message can be up to 1000 characters"
                                    "```")
                    return
                headers = {
                    'User-Agent': f'{ctx.guild.id} {command}_{typer} {value}'
                }
                async with aiohttp.ClientSession() as session:
                    async with session.put('http://localhost:6006/', headers=headers) as r:
                        if r.status == 200:
                            js = await r.json()
                            data = js[0]["data"]
                await ctx.reply("```"
                                "Configurations applied"
                                "```")
            else:
                await ctx.reply("Unkown type")
        elif command == "force_ban":
            if typer == "message":
                if len(value) > 1000:
                    await ctx.reply("```"
                                    f"Force-ban message can be up to 1000 characters"
                                    "```")
                    return
                headers = {
                    'User-Agent': f'{ctx.guild.id} {command}_{typer} {value}'
                }
                async with aiohttp.ClientSession() as session:
                    async with session.put('http://localhost:6006/', headers=headers) as r:
                        if r.status == 200:
                            js = await r.json()
                            data = js[0]["data"]
                await ctx.reply("```"
                                "Configurations applied"
                                "```")
            else:
                await ctx.reply("```"
                                "Unkown type"
                                "```")
        else:
            await ctx.reply("```"
                            "Unkown command"
                            "```")


def setup(bot: commands.Bot):
    log = logging.getLogger("shmoke")
    log.log(4242, "Config loaded")
    bot.add_cog(Config(bot))
