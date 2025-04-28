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


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

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
    
class User(db.Model):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    # email: Mapped[str] = mapped_column(String(120), index=True, unique=True) # ?
    password_hash: Mapped[Optional[str]] = mapped_column(String(256))
    
    # Understanding relationships:
    # https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html
    songs: Mapped[List["Song"]] = relationship(Song, back_populates = "user")
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def __init__(self, username):
        self.username = username



# test API call
# kpArt = coverArt("Firework", "Katy Perry")

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

# sanity check route 1
@app.route('/')
def index():
    return "hello"

# sanity check route 2, 
@app.route('/ping', methods=['GET', 'POST'])
def ping_pong():
    return jsonify('pong!')

@app.route('/songs', methods = ['GET', 'POST'])
def songs():
    return jsonify({
        'status': 'success',
        'songs': SONGS
    })

# alert("Searching for: "+ this.searchQuery); 
# var x = this.searchQuery.value
# x 
@app.route('/lyrics/<title>/<artist>', methods = ['GET', 'POST'])
def lyrics(title = None, artist = None):
    songLyrics = getLyrics(title, artist)
    return jsonify({
        'status': 'success',
        'lyrics': songLyrics
    })
    
@app.route('/admin')
def admin():
    all_users = db.session.query(User).all()
    return render_template('admin.html', all_users = all_users)


@app.route('/genius/search/<term>', methods = ['GET', 'POST'])
def searchSong(term = None):
    # parse data
    results = searchMulti(term)
    return jsonify({
        'status': 'success',
        'search_results': results
    })
    
#
# REST
#

@app.route('/api/user', methods = ['POST'])
def addUser():
    request_data = request.get_json()
    
    if request_data == None:
        return 'missing request', 400
    
    username = request_data['username']
    new_user = User(username)
    db.session.add(new_user)
    db.session.commit()
    
    return 'success', 204

@app.route('/api/user/<username>', methods = ['GET'])
def getUser():
    return

@app.route('/api/user/<username>', methods = ['POST'])
def updateUser():
    request_data = request.get_json()
    return

@app.route('/api/user/delete', methods = ['POST'])
def deleteUser():
    return

@app.route('/api/song/add', methods = ['POST'])
def addSong():
    return
    
@app.route('/api/song/get', methods = ['POST'])
def getSong():
    return

@app.route('/api/song/update', methods = ['POST'])
def updateSong():
    return

@app.route('/api/song/delete', methods = ['POST'])
def deleteSong():
    return

#
# RUN
#

if __name__ == '__main__':
    app.run(debug=True)