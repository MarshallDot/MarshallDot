import logging
import os
from discord.ext import commands

import enchant

bott: commands.Bot


def check(ctx):
    for i in enchant.Shell.servers():
        if int(i) == ctx.guild.id:
            return True
    return False


class Development(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bott = bot

    @commands.command()
    @commands.is_owner()
    async def reloadcogs(self, ctx: commands.Context):
        for filename in os.listdir(f'/home/fezciberk/valve/shell/cogs'):
            if filename.endswith('.py'):
                self.bot.reload_extension(f'cogs.{filename[:-3]}')
            elif filename == "__pycache__":
                pass
            else:
                print(f'Unable to reload {filename[:-3]}')
        await ctx.reply("```"
                        "Cogs reloaded"
                        "```")


def setup(bot: commands.Bot):
    log = logging.getLogger("shmoke")
    log.log(4242, "Development loaded")
    bot.add_cog(Development(bot))
