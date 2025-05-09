#
# A web server for 'those are the lyrics?' written in python using flask and sqlalchemy
# vue is configured to call this server on localhost:5001
# flask run --port=5001 --debug
#

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from genius import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional
import os
from werkzeug.security import generate_password_hash as hash_password, check_password_hash as verify_password

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

#
# DATABASE
#
# this is a combination of tutorials and code from joslenne's activity
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database <- flask DB setup
# https://realpython.com/flask-connexion-rest-api-part-3/ <- linking tables

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mondegreen.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # joslenne says we might need this? testing without

# Initialize SQLAlchemy with Declarative Base
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Song(db.Model):
    __tablename__ = "songs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="songs")
    
    # DATA:
    title: Mapped[str] = mapped_column(String, nullable=False)
    artist: Mapped[str] = mapped_column(String, nullable=False)
    img_path: Mapped[str] = mapped_column(String)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    
    def __repr__(self):
        return '<Song {} by {}>'.format(self.title, self.artist)
    
    def __init__(self, title: str, artist: str, img_path: str, score: int):
        self.title = title
        self.artist = artist
        self.img_path = img_path
        self.score = score
        
    def toJSON(self):
        jason = {
            'title': self.title,
            'artist': self.artist,
            'img_path': self.img_path,
            'score': self.score
        }
        return jason
    
class User(db.Model):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(256))
    
    # Understanding relationships:
    # https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html
    songs: Mapped[List["Song"]] = relationship(Song, back_populates = "user")
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def __init__(self, username: str, password_hash: str = None):
        self.username = username
        if password_hash:
            self.password_hash = password_hash    
        
    def toJSON(self):
        songs = []
        for song in self.songs:
            songs.append(song.toJSON())
        jason = {
            'username': self.username,
            'songs': songs
        }
        return jason

def createSong(title: str, artist: str, score: int, user_id: int):
    img_path = coverArt(title, artist)
    new_song = Song(title, artist, img_path, score)
    
    active_user = db.session.get(User, user_id)
    active_user.songs.append(new_song)
    db.session.commit()
    
def editSong(id: int, score: int):
    song = db.session.get(Song, id)
    song.score = score
    db.session.commit()

# test song data from pre-database server testing
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
    }
]

# Initialize database with sample data
@app.before_request
def setup():
    with app.app_context():
        db.create_all()
        if not db.session.query(User).all():  # If database is empty, add a sample entry
            u = User(username = 'redding')
            for data in SONGS:
                u.songs.append(
                    Song(
                        title = data.get('title'),
                        artist = data.get('artist'),
                        img_path = data.get('cover'),
                        score = data.get('score')
                    )
                )
            db.session.add(u)
            db.session.commit()

#
# ROUTES
# 
@app.route('/')
def index():
    return "hello"

@app.route('/ping', methods=['GET', 'POST'])
def ping_pong():
    return jsonify('pong!')

@app.route('/admin')
def admin():
    all_users = db.session.query(User).all()
    return render_template('admin.html', all_users = all_users)

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

    ### LOGIN SYSTEM
@app.route('/login', methods=['POST'])
def home():
    data = request.json
    username = data['username']
    password = data['password']
    
    user_data = User.query.filter_by(username=username).first()
    if user_data and verify_password(pwhash=user_data.password_hash, password=password):
        # success, add to session
        userid =  user_data.id
        return jsonify({
            'status': 'success',
            'id': userid # TODO: BAD BAD SECURITY
        })
    # wrong password, failure
    return jsonify({
            'status': 'failure',
            'message': 'wrong password'
        })
    
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data['username']
    password = data['password']
    # Check if the username already exists
    if not User.query.filter_by(username=username).first():
        # create new user
        new_user = User(username, hash_password(password))
        db.session.add(new_user)
        db.session.commit()
        # add to session
        userid = new_user.id
        return jsonify({
            'status': 'success',
            'id': userid # TODO: BAD BAD SECURITY
        })
    return jsonify({
        'status': 'failure',
        'message': 'account already exists'
    })
    
@app.route('/logout', methods=['POST'])
def logout():
    # actually does nothing because of,, reasons
    return jsonify({
        'status': 'success'
    })

@app.route('/addsong', methods = ['GET', 'POST'])
def addSong():
    if request.method == 'POST':
        data = request.json
        userid = data['userid']
        title = data['title']
        artist = data['artist']
        score = data['score']
        u = db.session.get(User, userid)
        
        if(not u):
            return jsonify({
                'status': 'failure',
                'message': 'user not found'
            })
        # query song table for: user id, song title, and artist
        song = Song.query.filter_by(user_id = userid).filter_by(title = title).filter_by(artist = artist).first()
 
        if song: # if the song exists
            editSong(id = song.id, score = score)
            return jsonify({
                'status': 'success',
                'message': 'update song'
            })
        createSong(title = title, artist = artist, score = score, user_id = userid)
        return jsonify({
                'status': 'success',
                'message': 'new song'
            })
        
@app.route('/songs', methods = ['POST'])
def songs():
    id = request.json['userid']
    if not id:
        return jsonify({
            'status': 'failure',
            'message': 'missing id'
        })
    u = db.session.get(User, id)
    if not u:
        return jsonify({
            'status': 'failure',
            'message': 'user not found'
        })
    user_songs = u.songs
    songs = []
    for song in user_songs:
        songs.append(song.toJSON())
    
    return jsonify({
        'status': 'success',
        'songs': songs
    })

#
# RUN
#

if __name__ == '__main__':
    app.run(debug=True, port=5001)