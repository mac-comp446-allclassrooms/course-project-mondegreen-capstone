#
# A web server for 'those are the lyrics?' written in python using flask and sqlalchemy
# vue is configured to call this server on localhost:5001
# flask run --port=5001 --debug
#

# from typing_extensions import Self
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from lyrics import *

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

#
# ROUTES
# 
@app.route('/')
def index():
    return "hello"

@app.route('/ping', methods=['GET', 'POST'])
def ping_pong():
    return jsonify('pong!')

@app.route('/lyrics/list', methods = ['GET', 'POST'])
def list():
    songList = getList()
    return jsonify({
        'status': 'success',
        'list': songList,
    })

    ### GENIUS API ROUTES
# calls the getLyrics function from genius.py; returns the lyrics and cover of the song
@app.route('/lyrics/<title>/<artist>', methods = ['GET', 'POST'])
def lyrics(title = None, artist = None):
    songLyrics = getLyrics(title, artist)
    return jsonify({
        'status': 'success',
        'lyrics': songLyrics,
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)