import logging

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
        db = enchant.database(ctx.guild.id)
        if service == "mod-log":
            if not db.get("mod_log"):
                if not value:
                    await ctx.reply("```"
                                    "Please specify a text channel"
                                    "```")
                    return
                value = value.split("<#")
                value = value[1].split(">")
                value = value[0]
                db.set("mod_log", True)
                db.set("mod_log_channel", value)
                await ctx.reply("```"
                                "Mod-log enabled"
                                "```")
            else:
                db.set("mod_log", False)
                await ctx.reply("```"
                                "Mod-log disabled"
                                "```")
        elif service == "message-log":
            if not db.get("message_log"):
                db.set("message_log", True)
                await ctx.reply("```"
                                "Message-log enabled"
                                "```")
            else:
                db.set("message_log", False)
                await ctx.reply("```"
                                "Message-log disabled"
                                "```")
        elif service == "spam-filter":
            if not db.get("spam_filter"):
                db.set("spam_filter", True)
                await ctx.reply("```"
                                "Spam-filter enabled"
                                "```")
            else:
                db.set("spam_filter", False)
                await ctx.reply("```"
                                "Spam-filter disabled"
                                "```")
        elif service == "profanity-filter":
            if not db.get("profanity_filter"):
                db.set("profanity_filter", True)
                await ctx.reply("```"
                                "Profanity-filter enabled"
                                "```")
            else:
                db.set("profanity_filter", False)
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
        database = enchant.database(ctx.guild.id)
        if value == "on":
            value = True
        elif value == "off":
            value = False
        if command == "all":
            if typer == "prefix":
                database.set(typer, value)
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
                database.set(f"{command}_{typer}", value)
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
                database.set(f"{command}_{typer}", value)
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
                database.set(f"{command}_{typer}", value)
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
                database.set(f"{command}_{typer}", value)
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
