import logging

import couchdb
import keyring
import pymongo
import redis

import network.database

db = logging.getLogger("database")

mongourl = keyring.get_password("MogoMar", "MogoMar")

mogoClient = pymongo.MongoClient(mongourl)
mogoDb = mogoClient["tortiy"]

dicy = dict()


class logg:
    def __init__(self, sid, sid2):
        self.id = sid
        self.id2 = sid2
        couch = couchdb.Server("http://admin:example@localhost:5984/")
        self.couch = couch["marshall"]
        self.r: redis.Redis = redis.Redis(host="127.0.0.1", port="5005")

    def new(self, type, log):
        log: str
        lo = dict()
        lo["log"] = log
        lo["type"] = type
        dataID = self.couch.save(lo)
        self.r.set(f"{self.id}_{self.id2}", dataID[0])

    def get(self, name):
        data = self.r.get(f"{self.id}_{self.id2}").decode()
        data = self.couch[data]
        return data[name]

    def delete(self):
        data = self.r.get(f"{self.id}_{self.id2}").decode()
        data = self.couch[data]
        self.couch.delete(data)


def get_log(sid, sid2):
    log = network.database.logg(sid, sid2)
    logtxt: str = log.get("log")
    typee: str = log.get('type')
    typee = typee.replace("_", " ")
    resul: str = ""
    resul += f"Type: {typee}\n"
    logpos = logtxt.split("\n")
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
