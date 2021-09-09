import logging

import redis

import responses
from blacksheep.server import Application
from blacksheep.messages import Request
from blacksheep.server.responses import json
import uvicorn

import network.database.database

engine = Application()


@engine.on_start()
async def startup(ar):
    db = logging.getLogger("database")
    db.setLevel(logging.DEBUG)
    dbHand = logging.FileHandler(filename='../../shmoke/logs/database.non.log',
                                 encoding='utf-8', mode='w')
    dbHand.setFormatter(logging.Formatter('%(asctime)s, %(process)s, %(levelname)s, %(name)s: %(message)s'))
    db.addHandler(dbHand)


@engine.route("/", methods=["GET"])
async def getEngine(request: Request):
    r = redis.Redis(host="localhost", port=5005)
    user_agent = request.headers.get(b'User-Agent')
    user_agent = user_agent[0].decode().split(" ")
    db = network.database.database(user_agent[0])
    get = await db.get(user_agent[1])
    data = responses.Basic(get)
    return json([data])


@engine.route("/", methods=["POST"])
async def postEngine(request: Request):
    user_agent = request.headers.get(b'User-Agent')
    user_agent[0]: bytes
    db = network.database.database(user_agent[0].decode())
    newter = await db.new()
    data = responses.Basic(f'{newter}')
    return json([data])


@engine.route("/", methods=["PUT"])
async def putEngine(request: Request):
    user_agent = request.headers.get(b'User-Agent')
    user_agent = user_agent[0].decode().split(" ")
    forleng = 0
    value = ""
    for i in user_agent:
        if forleng == 0:
            pass
        elif forleng == 1:
            pass
        else:
            value += i
        forleng += 1
    db = network.database.database(user_agent[0])
    if user_agent[1] == "True":
        user_agent[1] = True
    elif user_agent[1] == "False":
        user_agent[1] = False
    setter = await db.set(user_agent[1], value)
    data = responses.Basic(f"{setter}")
    return json([data])


@engine.route("/", methods=["DELETE"])
async def deleteEngine(request: Request):
    user_agent = request.headers.get(b'User-Agent')
    user_agent[0]: bytes
    db = network.database.database(user_agent[0].decode())
    delter = await db.delete()
    data = responses.Basic(delter)
    return json([data])


uvicorn.run(engine, port=6006, host="::1")
