import asyncio
import logging

import aiohttp
import discord
import keyring
import mariadb
import yaml
from aiopg.sa import create_engine

import enchant
from enchant import enchants

log = logging.getLogger("shmoke")


async def test():
    async with create_engine(host="127.0.0.1", port="3003", password="example",
                             database="mar", user="root") as engine:
        print(engine.name)


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


def marsun():
    loop = asyncio.new_event_loop()
    shell = enchant.Marshall(command_prefix=enchant.get_prefix, case_insensitive=True, intents=discord.Intents.all(), loop=loop)

    shell.config(Shell.token)
    shell.loadCogs()

    shell.apa()


def marshall():
    loop = asyncio.new_event_loop()
    task = loop.create_task(marsun())
    loop.run_until_complete(test())
    loop.run_forever()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(enchant.config())
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='./logs/discord.non.log', encoding='utf-8',
                                  mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(threadName)s - %(name)s: %(message)s'))
    logger.addHandler(handler)

    loggerSh = logging.getLogger("shmoke")
    logging.addLevelName(4242, "SHMOKE")
    loggerSh.setLevel(4242)
    handlerSh = logging.FileHandler(filename='./logs/shmoke.non.log', encoding='utf-8',
                                    mode='w')
    handlerSh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(threadName)s - %(name)s: %(message)s'))
    loggerSh.addHandler(handlerSh)

    db = logging.getLogger("database")
    db.setLevel(logging.DEBUG)
    dbHand = logging.FileHandler(filename='./logs/database.non.log',
                                 encoding='utf-8', mode='w')
    dbHand.setFormatter(logging.Formatter('%(asctime)s, %(process)s, %(levelname)s, %(name)s: %(message)s'))
    db.addHandler(dbHand)

    marshall()
