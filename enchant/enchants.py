import asyncio

import keyring
import redis
import yaml
from discord.ext import commands

build = False
threads = []
bot: commands.Bot
kill: bool = False
password = keyring.get_password('VALVEDB', 'VALVEDB')
with open("../network/database/data.yaml", 'r') as stream:
    try:
        data = yaml.safe_load(stream)
        prefix = data["prefix"]
        redispass = data["redis-password"]
        redisuser = data["redis-user"]
        redisport = data["redis-port"]
        redishost = data["redis-host"]
        if redisuser == "None" and redispass == "None":
            r = redis.Redis(host=redishost, port=redisport)
            r_funcs = redis.StrictRedis(host=redishost, port=redisport)
        elif redisuser == "None":
            r = redis.Redis(host=redishost, port=redisport, password=redispass)
            r_funcs = redis.StrictRedis(host=redishost, port=redisport, password=redispass)
        elif redispass == "None":
            r = redis.Redis(host=redishost, port=redisport, username=redispass)
            r_funcs = redis.StrictRedis(host=redishost, port=redisport, username=redispass)
        else:
            r = redis.Redis(host=redishost, port=redisport, username=redispass, password=redispass)
            r_funcs = redis.StrictRedis(host=redishost, port=redisport, username=redispass, password=redispass)
    except yaml.YAMLError as exc:
        print(exc)
