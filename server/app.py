#
# A web server for 'those are the lyrics?' written in python using flask and sqlalchemy
# vue is configured to call this server on localhost:5001
# flask run --port=5001 --debug
#

from flask import Flask, jsonify, render_template, request, session
from flask_cors import CORS
from genius import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional
import os
from flask_security.utils import hash_password, verify_password

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

SALT = os.urandom(32)
app.config['SECURITY_PASSWORD_SALT'] = SALT  # Salt for hashing passwords

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

def createSong(title: str, artist: str, score: int):
    img_path = coverArt(title, artist)
    new_song = Song(title, artist, img_path, score)
    
    active_user = db.session.get(User, session['id'])
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

    ### TESTING ROUTES, DELETE LATER
@app.route('/test/user/<username>')
def testuserquery(username = None):
    user_data = User.query.filter_by(username=username).first()
    return jsonify({
        'status': 'success',
        'user': user_data.toJSON()
    })
    
@app.route('/test/login/<username>')
def testlogin(username = None):
    user_data = User.query.filter_by(username=username).first()
    session['id'] = user_data.id
    return f'logged in {user_data.username}'

@app.route('/test/logout')
def testlogout():
    session.pop('id', None)
    return 'success'

@app.route('/test/getsong')
def testsong():
    if(session.get('id')):
        user = db.session.get(User, session['id'])
        asong = user.songs[0]
        return asong.toJSON()
    return 'not logged in!'
    
@app.route('/')
def index():
    return "hello"

@app.route('/ping', methods=['GET', 'POST'])
def ping_pong():
    return jsonify('pong!')

@app.route('/songs', methods = ['GET', 'POST'])
def songs():
    return jsonify({
        'status': 'success',
        'songs': SONGS
    })

@app.route('/admin')
def admin():
    all_users = db.session.query(User).all()
    return render_template('admin.html', all_users = all_users)

    ### GENIUS API ROUTES
@app.route('/lyrics/<title>/<artist>', methods = ['GET', 'POST'])
def lyrics(title = None, artist = None):
    songLyrics = getLyrics(title, artist)
    songCover = getCover(title, artist)
    return jsonify({
        'status': 'success',
        'lyrics': songLyrics,
        'cover': songCover
    })

@app.route('/genius/search/<term>', methods = ['GET', 'POST'])
def searchSong(term = None):
    # parse data
    results = searchMulti(term)
    return results

# TODO: change this redundancy
@app.route('/genius/search2/<term>', methods = ['GET', 'POST'])
def searchSong2(term = None):
    # parse data
    results = searchMulti2(term)
    return results

@app.route('/genius/genre/<genre>/', methods = ['GET', 'POST'])
def searchGenre2(genre = None):
    # parse data
    results = searchGenre(genre)
    return results

    ### LOGIN SYSTEM
@app.route('/login', methods=['POST'])
def home():
    username = request.form['username']
    password = request.form['password']
    user_data = User.query.filter_by(username=username).first()
    if user_data and verify_password(password, user_data.password):
        # success, add to session
        session['id'] = user_data.id
        return jsonify({
            'status': 'success'
        })
    # wrong password, failure
    return jsonify({
            'status': 'failure',
            'message': 'wrong password'
        })
    
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    # Check if the username already exists
    if not User.query.filter_by(username=username).first():
        # create new user
        new_user = User(username, hash_password(password))
        db.session.add(new_user)
        db.session.commit()
        # add to session
        session['id'] = new_user.id
        return jsonify({
            'status': 'success'
        })
    return jsonify({
        'status': 'failure',
        'message': 'account already exists'
    })
    
@app.route('/logout', methods=['POST'])
def logout():
    # remove from session
    session.pop('id', None)
    return jsonify({
        'status': 'success'
    })

@app.route('/song/<id>', methods = ['GET', 'POST'])
def addSong():
    if request.method == 'GET':
        if session.get('id'):
            u = db.session.get(User, session['id'])
            if False: # query songs here
                return 'found' # return song here
            return jsonify({
                'status': 'failure',
                'message': 'song not found'
            })
        return jsonify({
            'status': 'failure',
            'message': 'not logged in'
        })
    if request.method == 'POST':
        if session.get('id'):
            u = db.session.get(User, session['id'])
            
            data = request.get_json()
            # query song table for: user id, song title, and artist
            if False: # if the song exists
                # update song
                editSong(id = 0, score = 0)
                return jsonify({
                    'status': 'success',
                    'message': 'update song'
                })
            createSong(title = '', artist = '', score = 0)
            
            return jsonify({
                'status': 'success',
                'message': 'new song'
            })
        
        return jsonify({
            'status': 'failure',
            'message': 'not logged in'
        })
                    
    # find current user from session
    # search by id or artist/title?
    # GET: returns song json or "song not found"
    # -> all songs if nothing in <>?
    # POST: adds if new or updates if not new
    # don't need a delete functionality from the frontend, admin interface could have delete for debugging

#
# RUN
#

if __name__ == '__main__':
    app.run(debug=True, port=5001)