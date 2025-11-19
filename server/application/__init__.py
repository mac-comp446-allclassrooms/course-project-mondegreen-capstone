#
# A web server for 'those are the lyrics?' written in python using flask and sqlalchemy
# vue is configured to call this server on localhost:5001
# flask run --port=5001 --debug
#

# from typing_extensions import Self
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from server.application.song_data import SongData

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(__name__)
    if test_config is None:
        app.config['SOURCE_FILE'] = 'server/application/songs.txt'
    else:
        app.config['SOURCE_FILE'] = test_config

    songs = SongData(app.config['SOURCE_FILE'])

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
    def song_list():
        return jsonify({
            'status': 'success',
            'list': songs.get_songs(),
        })

        ### GENIUS API ROUTES
    # calls the getLyrics function from genius.py; returns the lyrics and cover of the song
    @app.route('/lyrics/<title>/<artist>', methods = ['GET', 'POST'])
    def lyrics(title = None, artist = None):
        #songLyrics = get_lyrics(app.config['SOURCE_FILE'], title, artist)

        try:
            song_lyrics = songs.get_lyrics(title + ":" + artist)
        except KeyError:
            return "Record not found", 400

        return jsonify({
            'status': 'success',
            'lyrics': song_lyrics,
        })

    return app