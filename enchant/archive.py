import logging

import aiofiles
import keyring
import pymongo
import redis
import yaml
from psycopg2 import connect

db = logging.getLogger("database")


mongourl = keyring.get_password("MogoMar", "MogoMar")


mogoClient = pymongo.MongoClient(mongourl)
mogoDb = mogoClient["tortiy"]


global r
global r_funcs
global conn
global mariad
global prefix


async def config():
    async with aiofiles.open('../network/database/data.yaml', mode='r') as f:
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


dicy = dict()


class logg:
    def __init__(self, sid, sid2, type, log):
        self.id = sid
        self.id2 = sid2
        self.type = type
        self.log = log
        self.cur = mariad.cursor()
        self.cur.execute("USE marshall")

    def new(self):
        self.log: str
        logho = self.log.replace("'", "`")
        query = f"INSERT INTO log (id, server_id, type, log)"\
                f"VALUES ('{self.id}', '{self.id2}', '{self.type}', '{logho}')"
        self.cur.execute(query)
        mariad.commit()

    def get(self, name):
        self.cur.execute(f"SELECT {name} FROM log WHERE id = {self.id} AND server_id = {self.id2} LIMIT 1")
        results = self.cur.fetchall()
        for i in results:
            return i[0]

    def delete(self):
        self.cur.execute(f"DELETE FROM log WHERE id = {self.id} AND server_id = {self.id2}")


def get_log(sid, sid2):
    cur = mariad.cursor()
    cur.execute("USE marshall")
    cur.execute(f"SELECT * FROM log WHERE id = {sid} AND server_id = {sid2} LIMIT 1")
    results = cur.fetchall()
    resul: str = ""
    results[0][2]: str
    results[0][3]: str
    typee = results[0][2].replace("_", " ")
    resul += f"Type: {typee}\n"
    logg: str = results[0][3].replace("_", " ")
    logpos = logg.split("\n")
    lenfor = 0
    for i in logpos:
        if i == "" or i == " ":
            pass
        else:
            if lenfor == 0:
                resul += f"Log: {i}"
            else:
                ii = f"\n     {i}"
                resul += ii
            lenfor += 1
    return resul


def upload(id, url):
    collection = mogoDb["photos"]
    data = dict()
    data["photoID"] = id
    data["url"] = url
    collection.insert(data)
    db.debug(f"New photo uploaded {data}")
