import logging

import keyring
import mariadb
import pymongo

db = logging.getLogger("database")


mongourl = keyring.get_password("MogoMar", "MogoMar")


mogoClient = pymongo.MongoClient(mongourl)
mogoDb = mogoClient["tortiy"]


mariad = mariadb.connect(user="root", password="example", host="localhost", port=4004)
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
        query = f"INSERT INTO log (id, server_id, type, log)"\
                f"VALUES ('{self.id}', '{self.id2}', '{self.type}', '{self.log}')"
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
    results[0][2]: str
    results[0][3]: str
    typee = results[0][2].replace("_", " ")
    logg = results[0][3].replace("_", " ")
    resul = ""
    resul += f"Type: {typee}"
    resul += f"\nLog: {logg}"
    return resul


def upload(id, url):
    collection = mogoDb["photos"]
    data = dict()
    data["photoID"] = id
    data["url"] = url
    collection.insert(data)
    db.debug(f"New photo uploaded {data}")
