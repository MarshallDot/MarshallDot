import logging

from discord.ext import commands

import enchant


class HelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        text = "```\n"
        text += ""
        prefix_not = f"Prefix for using commands: {self.clean_prefix}"
        for cog in mapping:
            cog: commands.Cog
            if not cog:
                continue
            elif cog.qualified_name == "events":
                continue
            lengh = len(mapping[cog])
            lenghf = 0
            command = ""
            for com in mapping[cog]:
                lenghf += 1
                if lenghf == lengh:
                    command += f"{com.qualified_name}"
                else:
                    command += f"{com.qualified_name}, "
            text += f"{cog.qualified_name}: {command}\n"
        text += "```"
        prefix_not = f"```{prefix_not}```"
        await self.get_destination().send(text)
        await self.get_destination().send(prefix_not)

    async def send_cog_help(self, cog):
        return await super().send_cog_help(cog)

    async def send_group_help(self, group):
        return await super().send_group_help(group)

    async def send_command_help(self, command):
        return await super().send_command_help(command)


def check(ctx):
    for i in enchant.Shell.servers():
        if int(i) == ctx.guild.id:
            return True
    return False


class Bot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.help_command = HelpCommand()
        bot.help_command.cog = self

    @commands.command()
    async def bug(self, ctx: commands.Context, *, bug):
        await ctx.bug(bug)
        await ctx.reply("The bug you found has been sent to the developer. Bug:\n"
                        "```"
                        f"{bug}"
                        "```")


def setup(bot: commands.Bot):
    log = logging.getLogger("shmoke")
    log.log(4242, "Bot loaded")
    bot.add_cog(Bot(bot))
