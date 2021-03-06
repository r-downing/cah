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
        game_data[gid] = {'draw': 0, 'black': 0, 'submitted': [], 'revealed': 0, 'start': int(time.time())}
    active[gid] = game_data[gid]
    response = jsonify(game_data[gid])
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/game/<int:gid>/new')
def new_game(gid):
    global game_data
    now = int(time.time())
    if now - game_data[gid]['start'] > 5:
        game_data[gid]['black'] = game_data[gid]['black'] + 1
        game_data[gid]['submitted'] = []
        game_data[gid]['winner'] = None
        game_data[gid]['revealed'] = 0
        game_data[gid]['start'] = now
    return game_status(gid)


@app.route('/game/<int:gid>/draw')
def draw(gid):
    global game_data
    game_data[gid]['draw'] = game_data[gid]['draw'] + 1
    return game_status(gid)


@app.route('/game/<int:gid>/submit/<sid>')
def submit(gid, sid):
    global game_data
    game_data[gid]['submitted'].append(sid)
    return game_status(gid)


@app.route('/game/<int:gid>/reveal')
def reveal(gid):
    global game_data
    game_data[gid]['revealed'] += 1
    return game_status(gid)


@app.route('/game/<int:gid>/winner/<sid>')
def winner(gid, sid):
    global game_data
    game_data[gid]['winner'] = sid
    return game_status(gid)
