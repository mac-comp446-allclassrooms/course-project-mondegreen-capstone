# Those are the Lyrics?

"Those are the Lyrics?" is a song lyric game made by Michelle Dong, Redding Sauter, and Kendall Sullivan in Joslenne Peña's Internet Computing capstone course at Macalester College. The purpose of the game is to search for a song and then try to guess the lyrics to that song the best you can. There is an optional login that is intended to save the statistics from the user (what songs they tried, what their scores were) however it is not fully implemented at this time so the game stats is hardcoded. However, the main game is still functional.

## Tech Stack

Our project is hosted on Vue.js.
The backend uses Flask and SqlAlchemy.
We use axios to make asynchronous calls to our Flask API.
The lyrics for each song are retrieved using the Genius API.
We use Vuex to store the lyrics, title, and artist to be used in the game.
Our project is styled using vanilla CSS, CSS grid layout, and CSS flexbox layout.

## Installation Instructions

For our project, you need to have Python and Node.js installed on your device.

In order to run our application, you must run the following:
```bash
cd mondegreen
npm install
```
```bash
pip install flask
pip install flask_cors
pip install flask_sqlalchemy
pip install sqlalchemy.orm werkzeug
pip install lyricsgenius
```

## Running the Project

To run our project, in one terminal window run the backend:

MacOS:
```bash
cd server
flask run --port=5001
```

Windows:
```bash
cd server
python -m flask run --port 5001
```

In a second terminal window run the frontend:

MacOS and Windows:
```bash
cd mondegreen
npm run dev
```
After doing so, use [localhost:5173](http://localhost:5173) to play "Those are the Lyrics?"!

