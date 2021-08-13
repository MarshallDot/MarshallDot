from flask import Flask, jsonify, request

import network.database.database

engine = Flask("engine")


@engine.route("/", methods=["GET"])
def getEngine():
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.split(" ")
    db = network.database.database(user_agent[0])
    get = db.get(user_agent[1])
    data = {"data": f"{get}"}
    cookiesWithMilk = {"status": "cookies", "with": "milk"}
    return jsonify(data, cookiesWithMilk)


@engine.route("/", methods=["POST"])
def postEngine():
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.split(" ")
    db = network.database.database(user_agent[0])
    newter = db.new()
    data = {'data': f'{newter}'}
    cookiesWithMilk = {"status": "cookies", "with": "milk"}
    return jsonify(data, cookiesWithMilk)


@engine.route("/", methods=["PUT"])
def putEngine():
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.split(" ")
    db = network.database.database(user_agent[0])
    setter = db.set(user_agent[1], user_agent[2])
    data = {'data': f'{setter}'}
    cookiesWithMilk = {"status": "cookies", "with": "milk"}
    return jsonify(data, cookiesWithMilk)


@engine.route("/", methods=["DELETE"])
def deleteEngine():
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.split(" ")
    db = network.database.database(user_agent[0])
    delter = db.delete()
    data = {'data': f'{delter}'}
    cookiesWithMilk = {"status": "cookies", "with": "milk"}
    return jsonify(data, cookiesWithMilk)


engine.run(host="::1", port=6006)
