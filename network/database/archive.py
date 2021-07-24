import logging

import keyring
import mariadb
import pymongo

db = logging.getLogger("database")


mogoClient = pymongo.MongoClient("mongodb+srv://tuncaydesto:tuncaydesto31@cluster0.nz05n.mongodb.net/tortiy?retryWrites=true&w=majority")
mogoDb = mogoClient["tortiy"]


passwordmaria = keyring.get_password('VALVEDB', 'VALVEDB')
mariad = mariadb.connect(user="root", password=passwordmaria, host="localhost", port=3306)
dicy = dict()


class logg:
    def __init__(self, sid, sid2, type, log):
        self.id = sid
        self.id2 = sid2
        self.type = type
        self.log = log
        self.cur = mariad.cursor()
        self.cur.execute("USE VALVE")

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
    cur.execute("USE VALVE")
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
