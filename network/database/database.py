import logging
import couchdb

import redis

db = logging.getLogger("database")

dicy = dict()


class pud:
    def __init__(self, sid):
        self.id = sid
        couch = couchdb.Server("http://admin:example@localhost:5984/")
        self.couch = couch["marshall"]
        self.r: redis.Redis = redis.Redis(host="127.0.0.1", port="5005")

    async def new(self):
        prefix = "!"
        settings = dict()
        settings["prefix"] = prefix
        settings["mod_log"] = False
        settings["profanity_filter"] = False
        settings["spam_filter"] = False
        settings["force_ban_message"] = None
        settings["kick_message"] = None
        settings["ban_message"] = None
        settings["mod_log_channel"] = None
        settings["message_log"] = None
        dataID, dataREV = self.couch.save(settings)
        self.r.set(f"{self.id}", dataID)
        db.debug(f"New server created on database: {self.id}, {dataID[0]}")
        return dataID

    async def set(self, name, value):
        dataID: bytes = self.r.get(f"{self.id}")
        data = self.couch[dataID.decode()]
        data[name] = value
        dataID, dataREV = self.couch.save(data)
        if self.r.get(f"{self.id}_{name}"):
            self.r.set(f"{self.id}_{name}", str(value))
        self.r.set(f"{self.id}", dataID)
        db.debug(f"A value has been changed: {data}")

    async def get(self, name):
        dataID: bytes = self.r.get(f"{self.id}")
        cache: bytes = self.r.get(f"{self.id}_{name}")
        if cache:
            cache = self.r.get(f"{self.id}_{name}").decode()
            if cache == "True":
                cache = True
            elif cache == "False":
                cache = False
        data = self.couch[dataID.decode()]
        self.r.set(f"{self.id}_{name}", str(data))
        db.debug(f"A value was taken: {data}")
        if data[name] == "True":
            data = True
        elif data[name] == "False":
            data = False
        else:
            data = data[name]
        return data

    async def delete(self):
        dataID: bytes = self.r.get(f"{self.id}")
        self.couch.delete(self.couch[dataID.decode()])
        self.r.delete(f"{self.id}")
        db.debug(f"A guild has been deleted: {self.id}")


class database:
    def __init__(self, sid):
        self.id = sid
        self.r: redis.Redis = redis.Redis(host="127.0.0.1", port="5005", db=0)
        self.mar = pud(sid)

    async def set(self, name, data):
        name: str
        data: str
        name = name.replace("-", "_")
        data = data.replace("-", "_")
        return await self.mar.set(name, data)

    async def get(self, name):
        name: str
        name = name.replace("-", "_")
        return await self.mar.get(name)

    async def delete(self):
        return await self.mar.delete()

    async def new(self):
        servers_db: bytes = self.r.get("servers")
        servers_db: str = servers_db.decode()
        servers = servers_db.split(", ")
        for i in servers:
            if int(i) == int(self.id):
                return await self.mar.new()
