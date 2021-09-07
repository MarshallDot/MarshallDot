import asyncio
import logging
from datetime import datetime

import aiohttp
import discord
from antispam import AntiSpamHandler
from antispam.ext import AntiSpamTracker
from discord.ext import commands
from profanity_filter import ProfanityFilter

import enchant.enchants


class events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.later_messageId = ""
        self.later_messageIds = ""
        self.bot = bot
        self.filter = ProfanityFilter(analyses="deep")
        self.filter._cache_redis = enchant.enchants.r

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.handler = AntiSpamHandler(self.bot, no_punish=True)
        self.bot.tracker = AntiSpamTracker(self.bot.handler, 3)
        self.bot.handler.register_extension(self.bot.tracker)
        print("Marshall ready now")
        log = logging.getLogger("shmoke")
        log.log(4242, "Marshall ready now")

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload: discord.RawMessageDeleteEvent):
        for i in enchant.Shell.servers():
            if int(i) == payload.guild_id:
                headers = {
                    'User-Agent': f'{payload.guild_id} mod_log'
                }
                async with aiohttp.ClientSession() as session:
                    async with session.get('http://localhost:6006/', headers=headers) as r:
                        if r.status == 200:
                            js = await r.json()
                            data = js[0]["data"]
                if data:
                    apid = self.bot.apid()
                    if self.later_messageId == str(payload.message_id):
                        return
                    else:
                        self.later_messageId = str(payload.message_id)
                    message = ""
                    with open(f'../data/{payload.guild_id}_messages.txt', "r") as fl:
                        lines = fl.readlines()
                        for i in lines:
                            if i.endswith(f"{payload.message_id}\n"):
                                pure_message = i.split(f" | message ID: {payload.message_id}\n")
                                pure_message = pure_message[0].split("```")
                                message += f"{pure_message[0]}\n"
                    with open(f'../data/{payload.guild_id}_messages.txt', "r") as fl:
                        lines = fl.readlines()
                        for i in lines:
                            if i.endswith(f"{payload.message_id}\n"):
                                pure_message = i.split(f" | message ID: {payload.message_id}\n")
                                message = pure_message[0]
                        if not message:
                            return
                        messapos = message.split(": ")
                        headers = {
                            'User-Agent': f'{payload.guild_id} prefix'
                        }
                        async with aiohttp.ClientSession() as session:
                            async with session.get('http://localhost:6006/', headers=headers) as r:
                                if r.status == 200:
                                    js = await r.json()
                                    prefix = js[0]["data"]
                        if messapos[1].startswith(prefix):
                            return
                    try:
                        headers = {
                            'User-Agent': f'{payload.guild_id} mod_log_channel'
                        }
                        async with aiohttp.ClientSession() as session:
                            async with session.get('http://localhost:6006/', headers=headers) as r:
                                if r.status == 200:
                                    js = await r.json()
                                    quer = js[0]["data"]
                    except:
                        return
                    log = enchant.logg(apid, payload.guild_id, "message_delete", message)
                    log.new()
                    chan = self.bot.get_channel(int(quer))
                    utc = datetime.utcnow()
                    utc = f'{utc.strftime("%Y-%m-%d")} {utc.strftime("%I:%M:%S")}'
                    await chan.send(f"`[{utc} UTC]` `[{apid}]` "
                                    f":wastebasket: Message deleted in {payload.channel_id}\n"
                                    f"```{message}```")

    @commands.Cog.listener()
    async def on_resumed(self):
        log = logging.getLogger("shmoke")
        log.log(4242, "Gateway Resumed")

    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, payload: discord.RawBulkMessageDeleteEvent):
        for i in enchant.Shell.servers():
            if int(i) == payload.guild_id:
                headers = {
                    'User-Agent': f'{payload.guild_id} mod_log'
                }
                async with aiohttp.ClientSession() as session:
                    async with session.get('http://localhost:6006/', headers=headers) as r:
                        if r.status == 200:
                            js = await r.json()
                            data = js[0]["data"]
                if data:
                    apid = self.bot.apid()
                    if self.later_messageIds == str(payload.message_ids):
                        return
                    else:
                        self.later_messageIds = str(payload.message_ids)
                    message = ""
                    with open(f'../data/{payload.guild_id}_messages.txt', "r") as fl:
                        lines = fl.readlines()
                        for i in lines:
                            for id in payload.message_ids:
                                if i.endswith(f"{id}\n"):
                                    pure_message = i.split(f" | message ID: {id}\n")
                                    headers = {
                                        'User-Agent': f'{payload.guild_id} prefix'
                                    }
                                    async with aiohttp.ClientSession() as session:
                                        async with session.get('http://localhost:6006/', headers=headers) as r:
                                            if r.status == 200:
                                                js = await r.json()
                                                prefix = js[0]["data"]
                                    message += f"{pure_message[0]}\n"
                    if message == "":
                        return
                    try:
                        headers = {
                            'User-Agent': f'{payload.guild_id} mod_log_channel'
                        }
                        async with aiohttp.ClientSession() as session:
                            async with session.get('http://localhost:6006/', headers=headers) as r:
                                if r.status == 200:
                                    js = await r.json()
                                    quer = js[0]["data"]
                    except:
                        return
                    log = enchant.logg(apid, payload.guild_id, "bulk_message_delete", message)
                    log.new()
                    chan = self.bot.get_channel(int(quer))
                    utc = datetime.utcnow()
                    utc = f'{utc.strftime("%Y-%m-%d")} {utc.strftime("%I:%M:%S")}'
                    await chan.send(f"`[{utc} UTC]` `[{apid}]` "
                                    f":wastebasket: Bulk message deleted in {payload.channel_id}\n"
                                    f"```{message}```")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if message.is_system():
            return
        if message.author.bot:
            return
        if not message.guild:
            await message.reply("```"
                                "You cannot use Marshall with direct message."
                                "```")
            return
        for i in enchant.Shell.servers():
            if int(i) == message.guild.id:
                message.author: discord.Member
                utc = datetime.utcnow()
                utc = f'{utc.strftime("%Y-%m-%d")} {utc.strftime("%I:%M:%S")}'
                headers = {
                    'User-Agent': f'{message.guild.id} message_log'
                }
                async with aiohttp.ClientSession() as session:
                    async with session.get('http://localhost:6006/', headers=headers) as r:
                        if r.status == 200:
                            js = await r.json()
                            data = js[0]["data"]
                if data:
                    with open(f'../data/{message.guild.id}_messages.txt', "a") as fl:
                        fl.write(f'[{utc} UTC] {message.author}: {message.content} | message ID: {message.id}\n')
                headers = {
                    'User-Agent': f'{message.guild.id} profanity_filter'
                }
                async with aiohttp.ClientSession() as session:
                    async with session.get('http://localhost:6006/', headers=headers) as r:
                        if r.status == 200:
                            js = await r.json()
                            data = js[0]["data"]
                if data:
                    if message.author.guild_permissions.kick_members:
                        pass
                    else:
                        profanity = self.filter.is_clean(message.content)
                        if profanity:
                            pass
                        else:
                            await message.delete()
                            await message.channel.send(f"Stop swearing {message.author.mention}")
                headers = {
                    'User-Agent': f'{message.guild.id} spam_filter'
                }
                async with aiohttp.ClientSession() as session:
                    async with session.get('http://localhost:6006/', headers=headers) as r:
                        if r.status == 200:
                            js = await r.json()
                            data = js[0]["data"]
                if data:
                    if message.author.guild_permissions.kick_members:
                        pass
                    else:
                        await self.bot.handler.propagate(message)

                        if self.bot.tracker.is_spamming(message):
                            await message.delete()
                            await message.channel.send(f"Stop spamming {message.author.mention}")
                            self.bot.tracker.remove_punishments(message)
            pass

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        for i in enchant.Shell.servers():
            if int(i) == guild.id:
                headers = {
                    'User-Agent': f'{guild.id}'
                }
                async with aiohttp.ClientSession() as session:
                    async with session.post('http://localhost:6006/', headers=headers) as r:
                        if r.status == 200:
                            js = await r.json()
                            data = js[0]["data"]
                return
        await asyncio.sleep(3600)
        guil = self.bot.get_guild(id=guild.id)
        await guil.leave()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        for i in enchant.Shell.servers():
            if int(i) == guild.id:
                headers = {
                    'User-Agent': f'{guild.id}'
                }
                async with aiohttp.ClientSession() as session:
                    async with session.delete('http://localhost:6006/', headers=headers) as r:
                        if r.status == 200:
                            js = await r.json()
                            data = js[0]["data"]
                return
        pass

    @commands.Cog.listener()
    async def on_message_join(self, member: discord.Member):
        pos = enchant.enchants.r.get(f"{member.guild.id}_forced").split(", ")
        for i in pos:
            if member.id == int(i):
                await member.ban(reason="Force Ban")


def setup(bot: commands.Bot):
    log = logging.getLogger("shmoke")
    log.log(4242, "Events loaded")
    bot.add_cog(events(bot))
