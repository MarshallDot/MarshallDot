import keyring
from discord.ext import commands

from network import database

build = False
threads = []
bot: commands.Bot
kill: bool = False
password = keyring.get_password('VALVEDB', 'VALVEDB')
r = database.r
r_funcs = database.r_funcs
