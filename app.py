import time
from threading import Thread

from flask import Flask, jsonify

app = Flask(__name__)


game_data = {}
active = {}


def cleanup():
    global game_data
    global active
    while 1:
        time.sleep(900)
        game_data = active
        active = {}


Thread(target=cleanup).start()


@app.route('/game/<int:gid>')
def game_status(gid):
    global game_data
    global active
    if gid not in game_data:
        game_data[gid] = {'draw': 0, 'black': 0, 'submitted': []}
    active[gid] = game_data[gid]
    response = jsonify(game_data[gid])
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/game/<int:gid>/new')
def new_game(gid):
    global game_data
    game_data[gid]['black'] = game_data[gid]['black'] + 1
    game_data[gid]['submitted'] = []
    game_data[gid]['winner'] = None
    game_data[gid]['revealed'] = 0
    return game_status(gid)


@app.route('/game/<int:gid>/draw')
def draw(gid):
    global game_data
    game_data[gid]['draw'] = game_data[gid]['draw'] + 1
    response = jsonify(game_data[gid]['draw'])
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/game/<int:gid>/submit/<int:sid>')
def submit(gid, sid):
    global game_data
    game_data[gid]['submitted'].append(sid)
    response = jsonify(True)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/game/<int:gid>/reveal')
def reveal(gid):
    global game_data
    game_data[gid]['revealed'] = 1
    response = jsonify(True)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/game/<int:gid>/winner/<int:sid>')
def winner(gid, sid):
    global game_data
    game_data[gid]['winner'] = sid
    response = jsonify(True)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response