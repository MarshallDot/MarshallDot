import asyncio
import logging
import signal

import discord
import keyring

import enchant
from enchant import enchants
from network import database

log = logging.getLogger("shmoke")


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


def marsun() -> enchant.Changing:
    loop = asyncio.new_event_loop()
    database.logger()
    shell = enchant.Changing(command_prefix=enchant.get_prefix, case_insensitive=True, intents=discord.Intents.all(), loop=loop)

    shell.config(Shell.token)
    shell.loadCogs()

    shell.apa()


def marshall():
    loop = asyncio.new_event_loop()
    loop.add_signal_handler(signal.SIGINT, lambda: loop.stop())
    loop.add_signal_handler(signal.SIGTERM, lambda: loop.stop())
    task = loop.create_task(marsun())
    loop.run_forever()


if __name__ == '__main__':
    marshall()
