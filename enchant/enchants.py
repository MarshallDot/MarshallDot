import asyncio

import keyring
import redis
import yaml
from discord.ext import commands

build = False
threads = []
r: redis.Redis
bot: commands.Bot
kill: bool = False
password = keyring.get_password('VALVEDB', 'VALVEDB')
with open("../network/database/data.yaml", 'r') as stream:
    try:
        data = yaml.safe_load(stream)
        prefix = data["prefix"]
        redisport = data["redis-port"]
        redishost = data["redis-host"]
        r = redis.Redis(host=redishost, port=redisport)
    except yaml.YAMLError as exc:
        print(exc)
