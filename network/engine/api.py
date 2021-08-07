from flask import Flask, jsonify, request

import network.database.database

engine = Flask("engine")


@engine.route("/", methods=["GET"])
def getEngine():
    input_json = request.get_json(force=True)
    db = network.database.database(input_json["id"])
    getter = db.get(input_json["name"])
    data = {'result': f'{getter}'}
    cookiesWithMilk = {"status": "cookies", "with": "milk"}
    return jsonify(data, cookiesWithMilk)


@engine.route("/", methods=["POST"])
def postEngine():
    input_json = request.get_json(force=True)
    db = network.database.database(input_json["id"])
    newter = db.new()
    data = {'result': f'{newter}'}
    cookiesWithMilk = {"status": "cookies", "with": "milk"}
    return jsonify(data, cookiesWithMilk)


@engine.route("/", methods=["PUT"])
def putEngine():
    input_json = request.get_json(force=True)
    db = network.database.database(input_json["id"])
    setter = db.set(input_json["name"], input_json["value"])
    data = {'result': f'{setter}'}
    cookiesWithMilk = {"status": "cookies", "with": "milk"}
    return jsonify(data, cookiesWithMilk)


@engine.route("/", methods=["DELETE"])
def deleteEngine():
    input_json = request.get_json(force=True)
    db = network.database.database(input_json["id"])
    delter = db.delete()
    data = {'result': f'{delter}'}
    cookiesWithMilk = {"status": "cookies", "with": "milk"}
    return jsonify(data, cookiesWithMilk)


engine.run(host="::1", port=6006)
