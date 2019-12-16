from .config import *
from flask import Flask, render_template, url_for, jsonify
import json
import requests
import sqlite3
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

riot_api_key = config['riot_api_key']
app.config['SQLALCHEMY_DATABASE_URI'] = config['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config['SQLALCHEMY_TRACK_MODIFICATIONS']
db = SQLAlchemy(app)

from .models import *

db.create_all()

from .api import blueprint_api

# Part1 Frontend
accountId = ''
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/matchHistory/<query>')
@app.route('/matchHistory/<query>/<keyOverride>')
def matchHistory(query, keyOverride=None):
    global accountId
    accountId = getAccountIdFromName(query, keyOverride)
    if(accountId):
        response = requests.get( \
            url = "https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/" + accountId + "?endIndex=10&beginIndex=0", \
            headers = {'X-Riot-Token': (keyOverride or riot_api_key)})
        if(response):
            if(response.status_code == 200):
                data = response.json()
                matches = list(data['matches'])
                strippedMatches = list(map(extractMatchIdAndChampionId, matches));
                for m in strippedMatches:
                    match = getMatch(str(m['matchId']), keyOverride)
                    participantIdentities = list(match['participantIdentities'])
                    participantId = list(filter(filerParticipantId, participantIdentities))[0]['participantId']
                    participantList = list(match['participants'])
                    participant = list(filter(lambda x: filerParticipant(x, participantId), participantList))[0]
                    m['win'] = participant['stats']['win']
                    m['k'] = participant['stats']['kills']
                    m['d'] = participant['stats']['deaths']
                    m['a'] = participant['stats']['assists']
                    m['champion'] = getChampionById(m['champion'])
                return jsonify(strippedMatches)
            else:
                return (jsonify({"message": "Request Failed"}), 400),
    return jsonify({"message": "Cannot find accout"}), 400


def extractMatchIdAndChampionId(m):
    return {
        "matchId": m['gameId'],
        "champion": m['champion']
    }

def filerParticipantId(p):
    if(p['player']['accountId'] == accountId):
        return True
    else:
        return False

def filerParticipant(p, participantId):
    if(p['participantId'] == participantId):
        return True
    else:
        return False

def getAccountIdFromName(query, keyOverride=None):
    response = requests.get( \
        url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + query, \
        headers = {'X-Riot-Token': (keyOverride or riot_api_key)})
    if(response):
        if(response.status_code == 200):
            data = response.json()
            return data['accountId']
        else:
            return None

def getMatch(query, keyOverride=None):
    response = requests.get( \
        url = "https://na1.api.riotgames.com/lol/match/v4/matches/" + query, \
        headers = {'X-Riot-Token': (keyOverride or riot_api_key)})
    if(response):
        if(response.status_code == 200):
            data = response.json()
            return data
        else:
            return None

def getChampionById(id):
    with open("app/static/champion.json") as championFile:
        data = json.load(championFile)
        for c in data['data']:
            if(str(id) == data['data'][c]['key']):
                return c
    return "Champion Not Found"

# Part2 Backend
app.register_blueprint(blueprint_api, url_prefix='/api/v1')
