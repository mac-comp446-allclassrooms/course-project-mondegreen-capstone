from flask import Flask, jsonify
from flask_cors import CORS
from genius import *


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

kpArt = coverArt("Firework", "Katy Perry")

SONGS = [
    {
        'title': 'symbol',
        'artist': 'Adrianne Lenker',
        'cover':  'https://images.genius.com/ea813421a18bde3bc39b73c110b0ab2c.300x300x1.jpg',
        'score': 100
    },
    {
        'title': 'Cloudbusting',
        'artist': 'Kate Bush',
        'cover':  'https://images.genius.com/c3e6f6097640bca27833078355fd647e.300x300x1.png',
        'score': 75
    },
    {
        'title': 'Simulation Swarm',
        'artist': 'Big Thief',
        'cover':  'https://images.genius.com/26084cc61b6b1849e2c762fd0ca709fc.300x300x1.png',
        'score': 80
    },
    {
        'title': 'Pump Up the Jam',
        'artist': 'Technotronic',
        'cover':  'https://images.genius.com/a3992138b1d56a1238150be0051cb321.300x300x1.png',
        'score': 25
    },
    {
        'title': 'Juna',
        'artist': 'Clairo',
        'cover':  'https://images.genius.com/6725f1000db2e875f4ce966f4144d41a.300x300x1.png',
        'score': 37
    },
    {
        'title': 'Hello Hello Hello',
        'artist': 'Remi Wolf',
        'cover':  'https://images.genius.com/9d9b505e394955ec1e750059846258c6.300x300x1.png',
        'score': 100
    },
    {
        'title': 'Linger',
        'artist': 'The Cranberries',
        'cover':  'https://images.genius.com/faeabffde6e1ce2c6ffafe4b5d01d4ab.300x300x1.png',
        'score': 34
    },
    {
        'title': 'Blister In The Sun',
        'artist': 'Violent Femmes',
        'cover':  'https://images.genius.com/af35b7cdb9d07071e3946098f542377b.300x295x1.jpg',
        'score': 99
    },
    {
        'title': 'Firework',
        'artist': 'Katy Perry',
        'cover': kpArt,
        'score': 23 
    } 
]


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/songs', methods = ['GET'])
def songs():
    return jsonify({
        'status': 'success',
        'songs': SONGS
    })
    
@app.route('/lyrics/<title>/<artist>')
def lyrics(title = None, artist = None):
    songLyrics = getLyrics(title, artist)
    return jsonify({
        'status': 'success',
        'lyrics': songLyrics
    })


if __name__ == '__main__':
    app.run()