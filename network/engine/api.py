import responses
from blacksheep.server import Application
from blacksheep.messages import Request
from blacksheep.server.responses import json
import uvicorn

import network.database.database
import network.database.tables as tables

engine = Application()


@engine.on_start()
async def startup(ar):
    engine.debug(ar)
    await network.database.config()
    await tables.config()
    await tables.createTables()


@engine.route("/", methods=["GET"])
async def getEngine(request: Request):
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.split(" ")
    db = network.database.database(user_agent[0])
    get = db.get(user_agent[1])
    if user_agent[1] == "mod_log" or user_agent[1] == "profanity_filter" or user_agent[1] == "spam_filter" or user_agent[1] == "message_log":
        get = bool(get)
        print(get)
    if type(get) == bool or type(get) == int or type(get) == float:
        data = responses.Basic(get)
    else:
        data = responses.Basic(f"get")
    return json([data])


@engine.route("/", methods=["POST"])
async def postEngine(request: Request):
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.split(" ")
    db = network.database.database(user_agent[0])
    newter = db.new()
    data = responses.Basic(f'{newter}')
    return json([data])


@engine.route("/", methods=["PUT"])
async def putEngine(request: Request):
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.split(" ")
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
    setter = db.set(user_agent[1], value)
    data = responses.Basic(f"{setter}")
    return json([data])


@engine.route("/", methods=["DELETE"])
def deleteEngine(request: Request):
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.split(" ")
    db = network.database.database(user_agent[0])
    delter = db.delete()
    data = responses.Basic(f"{delter}")
    return json([data])


uvicorn.run(engine, port=6006, host="::1")
