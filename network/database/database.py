import logging
import yaml
from psycopg2 import connect

import keyring
import redis
import aiofiles

db = logging.getLogger("database")

global r
global r_funcs
global conn
global mariad
global prefix


async def config():
    async with aiofiles.open('../database/data.yaml', mode='r') as f:
        try:
            cont = await f.read()
            data = yaml.safe_load(cont)
            prefix = data["prefix"]
            postgrepass = data["postgre-password"]
            postgredb = data["postgre-database"]
            postgreuser = data["postgre-user"]
            postgreport = data["postgre-port"]
            postgrehost = data["postgre-host"]
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
            if postgreuser == "None" and postgrepass == "None":
                conn = connect(
                    dbname=postgredb,
                    user=postgreuser,
                    host="172.28.1.4",
                    password=postgrepass
                )
            elif postgreuser == "None":
                conn = connect(
                    dbname=postgredb,
                    user=postgreuser,
                    host="172.28.1.4",
                    password=postgrepass
                )
            elif postgrepass == "None":
                conn = connect(
                    dbname=postgredb,
                    user=postgreuser,
                    host="172.28.1.4",
                    password=postgrepass
                )
            else:
                conn = connect(
                    dbname=postgredb,
                    user=postgreuser,
                    host="172.28.1.4",
                    password=postgrepass
                )
            mariad = conn
        except yaml.YAMLError as exc:
            print(exc)


class Shell(object):
    token = keyring.get_password("SHELL", "SHELL")
    id = 862785705910599740
    owners = [487325278524276756]

    @staticmethod
    def servers():
        servers_db: bytes = r.get("servers")
        servers_db: str = servers_db.decode()
        servers = servers_db.split(", ")
        return servers


dicy = dict()


class maria:
    def __init__(self, sid):
        self.id = sid
        self.cur = mariad.cursor()

    def new(self):
        query = f"INSERT INTO server (id, mod_log, profanity_filter, message_log, spam_filter, " \
                "mod_log_channel, ban_message, kick_message, prefix, force_ban_message)" \
                f"VALUES ('{self.id}', false, false, false, false, 'None','None', 'None', '{prefix}', 'None')"
        self.cur.execute(query)
        mariad.commit()

    def set(self, name, value):
        self.cur.execute(f"UPDATE server SET {name} = '{value}' WHERE id = '{self.id}'")
        mariad.commit()

    def get(self, name):
        self.cur.execute(f"SELECT {name} FROM server WHERE id = '{self.id}' LIMIT 1")
        results = self.cur.fetchall()
        for i in results:
            return i[0]

    def delete(self):
        self.cur.execute(f"DELETE FROM server WHERE id = {self.id}")


class database:
    def __init__(self, sid):
        self.id = sid
        self.r = r
        self.r_funcs = r_funcs
        self.mar = maria(sid)

    def set(self, name, data):
        try:
            name = name.replace("-", "_")
            if type(data) == bool:
                if data:
                    data = "1"
                else:
                    data = "0"
            elif type(data) == str:
                data = data.replace("-", "_")
            ret: bytes = r.get(f"{self.id}_{name}")
            if ret:
                r.set(f"{self.id}_{name}", f"{data}")
            self.mar.set(name, data)
        except:
            return False
        nndata = dict()
        nndata["id"] = self.id
        nndata["name"] = name
        nndata["value"] = data
        db.debug(f"A data in the database has been changed {nndata}")
        return True

    def get(self, name):
        try:
            ret: bytes = r.get(f"{self.id}_{name}")
            if ret.decode() == '1':
                nndata = dict()
                nndata["id"] = self.id
                nndata["name"] = name
                db.debug(f"Data pulled from database {nndata}")
                return True
            elif ret.decode() == '0':
                nndata = dict()
                nndata["id"] = self.id
                nndata["name"] = name
                db.debug(f"Data pulled from database {nndata}")
                return False
            else:
                nndata = dict()
                nndata["id"] = self.id
                nndata["name"] = name
                db.debug(f"Data pulled from database {nndata}")
                return ret.decode()
        except:
            retm = str(self.mar.get(name))
            if retm == "0":
                r.set(f"{self.id}_{name}", "0")
                nndata = dict()
                nndata["id"] = self.id
                nndata["name"] = name
                db.debug(f"Data pulled from database {nndata}")
                return False
            elif retm == "1":
                r.set(f"{self.id}_{name}", "1")
                nndata = dict()
                nndata["id"] = self.id
                nndata["name"] = name
                db.debug(f"Data pulled from database {nndata}")
                return True
            r.set(f"{self.id}_{name}", f"{retm}")
            nndata = dict()
            nndata["id"] = self.id
            nndata["name"] = name
            db.debug(f"Data pulled from database {nndata}")
            return retm

    def delete(self):
        self.mar.delete()
        try:
            r.delete(f"{self.id}_profanity_filter")
            r.delete(f"{self.id}_message_log")
            r.delete(f"{self.id}_prefix")
            r.delete(f"{self.id}_mod_log")
            r.delete(f"{self.id}_ban_message")
            r.delete(f"{self.id}_kick_message")
            r.delete(f"{self.id}_temp_ban_message")
            r.delete(f"{self.id}_force_ban_message")
            r.delete(f"{self.id}_forced")
            r.delete(f"{self.id}_spam_filter")
        except:
            pass
        nndata = dict()
        nndata["id"] = self.id
        db.debug(f"Server deleted on database {nndata}")
        return True

    def new(self):
        for i in Shell.servers():
            if int(i) == self.id:
                try:
                    self.mar.new()
                except:
                    return False
                nndata = dict()
                nndata["id"] = self.id
                db.debug(f"New server created on database {nndata}")
        return True
