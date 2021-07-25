import logging
import os

import discord
import keyring
from discord.ext import commands
from sonyflake import SonyFlake

import enchant.enchants
from enchant import enchants
from network.database import *

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='../logs/discord.log', encoding='utf-8',
                              mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(threadName)s - %(name)s: %(message)s'))
logger.addHandler(handler)

loggerSh = logging.getLogger("shmoke")
logging.addLevelName(4242, "SHMOKE")
loggerSh.setLevel(4242)
handlerSh = logging.FileHandler(filename='../logs/shmoke.log', encoding='utf-8',
                                mode='w')
handlerSh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(threadName)s - %(name)s: %(message)s'))
loggerSh.addHandler(handlerSh)


class Shell(object):
    token = keyring.get_password("SHELL", "SHELL")
    id = 862785705910599740
    owners = [487325278524276756]

    @staticmethod
    def servers():
        servers_db: bytes = enchants.r.get("servers")
        servers_db: str = servers_db.decode()
        servers = servers_db.split(", ")
        return servers


class Marscontext(commands.Context):
    async def bug(self, value):
        try:
            with open("../logs/bugs.txt", "a") as fl:
                fl.write(f"An bug was found by {self.message.author}: {value}\n")
            await self.message.add_reaction("<:bughunter:853071857556914177>")
        except discord.HTTPException:
            pass


class Marshall(commands.Bot):
    def config(self, token):
        self.owner_ids = Shell.owners
        self.apatok = token
        enchants.bot = self

    def loadCogs(self):
        for filename in os.listdir(f'../cogs'):
            if filename.endswith('.py'):
                self.load_extension(f'cogs.{filename[:-3]}')
            elif filename == "__pycache__":
                pass
            else:
                print(f'Unable to load {filename[:-3]}')

    def apa(self):
        self.run(self.apatok)

    def apid(self):
        self.sf = SonyFlake()
        apid = str(self.sf.next_id())
        return apid[:-9]

    async def get_context(self, message, *, cls=Marscontext):
        return await super().get_context(message, cls=cls)


def shmokeL(message):
    loggerSh.log(4242, message)


def get_prefix(client, message: discord.Message):
    try:
        server = database(message.guild.id)
        prefix = server.get("prefix")
        return commands.when_mentioned_or(prefix)(client, message)
    except:
        return commands.when_mentioned_or("*")(client, message)
