#
# A web server for 'those are the lyrics?' written in python using flask and sqlalchemy
# vue is configured to call this server on localhost:5001
# flask run --port=5001 --debug
#

from flask import Flask, jsonify, render_template, request, flash
from flask_cors import CORS
from genius import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional
from flask_login import LoginManager, UserMixin
import os
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_security import Security, SQLAlchemyUserDatastore, login_required, login_user, current_user, logout_user
from flask_security.utils import hash_password, verify_password


# instantiate the app
app = Flask(__name__)
login = LoginManager(app)
app.config.from_object(__name__)

app.config['SECRET_KEY'] = 'supersecret'  # Secret key for session management and JWT
app.config['SECURITY_PASSWORD_SALT'] = 'salt'  # Salt for hashing passwords
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'SECRETKEYFORENCRYPTION'  # Secret key for JWT encoding

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Celery and Redis configuration
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',  # Redis as the message broker
    result_backend='redis://localhost:6379'  # Redis as the result backend
)

# TODO: how to generate and store secure keys?
SECRET_KEY = os.urandom(32)
# app.config['SECRET_KEY'] = SECRET_KEY

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
jwt = JWTManager(app)

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
    
class User(UserMixin, db.Model):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    # email: Mapped[str] = mapped_column(String(120), index=True, unique=True) # ?
    password_hash: Mapped[Optional[str]] = mapped_column(String(256))
    
    # active: Mapped[bool] = mapped_column(Boolean)  # Indicates if the user's account is active
    # fs_uniquifier: Mapped[str] = mapped_column(String(255))  # Unique identifier used by Flask-Security
    # last_login: Mapped[datetime] = mapped_column(DateTime(timezone=True))  # Timestamp of the user's last login
    # API_token: Mapped[str] = mapped_column(String, default=None)  # Stores the JWT token for API authentication
    
    # Understanding relationships:
    # https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html
    songs: Mapped[List["Song"]] = relationship(Song, back_populates = "user")
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def __init__(self, username):
        self.username = username
        
# Setup Flask-Security
# user_datastore = SQLAlchemyUserDatastore(db, User)
# security = Security(app, user_datastore)
    
# TODO: leftover from werkzeug, delete?
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


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
    return results
#
# REST
#
@app.route('/genius/search2/<term>', methods = ['GET', 'POST'])
def searchSong2(term = None):
    # parse data
    results = searchMulti2(term)
    return results

# @app.route('/login', methods=['POST'])
# def home():
#     username = request.form['username']
#     email = request.form['email']
#     password = request.form['password']
#     user_data = User.query.filter_by(email=email).first()
#     if user_data and verify_password(password, user_data.password):
#         login_user(user_data)
#         token = create_access_token(identity=user_data.username)  # Generate JWT token
#         user_data.API_token = token
#         user_data.last_login = datetime.now()
#         db.session.commit()
#         # success
#         return jsonify({
#             'status': 'success'
#         })
#     # wrong password, failure
#     return jsonify({
#             'status': 'failure',
#             'message': 'wrong password'
#         })
    
# @app.route('/signup', methods=['POST'])
# def signup():
#     username = request.form['username']
#     email = request.form['email']
#     password = request.form['password']
#     # Check if the username already exists
#     if not User.query.filter_by(email=email).first() and not User.query.filter_by(username=username).first():
#         new_user = user_datastore.create_user(
#             email=email,
#             username=username,
#             password=hash_password(password),  # Securely hash the password
#         )
#         db.session.commit()
#         return jsonify({
#             'status': 'success'
#         })
#     return jsonify({
#         'status': 'failure',
#         'message': 'account already exists'
#     })
    
# @app.route('/logout', methods=['POST'])
# def logout():
#     logout_user()
#     return jsonify({
#         'status': 'success'
#     })

@app.route('/song/<id>', methods = ['GET', 'POST'])
def addSong():
    if(current_user):
        return 'logged in'
    return 'logged out'
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