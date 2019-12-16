from flask import jsonify, request
from . import blueprint_api
from ..models import *

@blueprint_api.route('/listNames',methods=["GET"])
def listNames():
    recordList = list(SearchRecord.query.all())
    return jsonify(list(map(lambda x : x.toDict(), recordList))), 200

@blueprint_api.route('/addName', methods=["POST"])
def addName():
    if(request and request.json and ("summoner_name" in request.json)):
        insertName = request.json['summoner_name']
        searchRecord = SearchRecord(summoner_name=insertName)
        db.session.add(searchRecord)
        db.session.commit()
        return "", 200
    return "Bad Request", 400

@blueprint_api.route('/updateName', methods=["PUT"])
def updateName():
    if(request and request.json and ("summoner_name" in request.json) and ("new_name" in request.json)):
        updateName = request.json['summoner_name']
        newName = request.json['new_name']
        searchRecord = SearchRecord.query.filter_by(summoner_name=updateName).first()
        if(searchRecord):
            searchRecord.summoner_name = newName
            db.session.commit()
            return "", 200
        else:
            return "Record Not Found", 200
    return "Bad Request", 400

@blueprint_api.route('/deleteName', methods=["DELETE"])
def deleteName():
    if(request and request.json and ("summoner_name" in request.json)):
        deleteName = request.json['summoner_name']
        searchRecord = SearchRecord.query.filter_by(summoner_name=deleteName).first()
        if(searchRecord):
            db.session.delete(searchRecord)
            db.session.commit()
            return "", 200
        else:
            return "Record Not Found", 200
    return "Bad Request", 400
