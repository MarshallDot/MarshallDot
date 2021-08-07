import keyring
import redis
from discord.ext import commands

from network import database

build = False
threads = []
bot: commands.Bot
kill: bool = False
password = keyring.get_password('VALVEDB', 'VALVEDB')
r = redis.Redis(host='localhost', port=5005)
r_funcs = redis.StrictRedis(host='localhost', port=5005)
