#
# A web server for 'those are the lyrics?' written in python using flask and sqlalchemy
# vue is configured to call this server on localhost:5001
# flask run --port=5001 --debug
#

# from typing_extensions import Self
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from genius import *

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

    ### GENIUS API ROUTES
# calls the getLyrics function from genius.py; returns the lyrics and cover of the song
@app.route('/lyrics/<title>/<artist>', methods = ['GET', 'POST'])
def lyrics(title = None, artist = None):
    songLyrics = getLyrics(title, artist)
    songCover = getCover(title, artist)
    return jsonify({
        'status': 'success',
        'lyrics': songLyrics,
        'cover': songCover
    })

# calls the searchMulti function from genius.py; returns a list of songs that match the search term
@app.route('/genius/search/<term>', methods = ['GET', 'POST'])
def searchSong(term = None):
    # parse data
    results = searchMulti(term)
    return results

## eliminated because of the redundant searchSong function
# @app.route('/genius/search2/<term>', methods = ['GET', 'POST'])
# def searchSong2(term = None):
#     results = searchMulti2(term)
#     return results

# calls the searchGenre function from genius.py; returns a list of songs in the genre
@app.route('/genius/genre/<genre>/', methods = ['GET', 'POST'])
def searchGenre2(genre = None):
    results = searchGenre(genre)
    return results

#
# RUN
#

if __name__ == '__main__':
    app.run(debug=True, port=5001)