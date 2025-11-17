import string
import unicodedata
from server.lyrics import get_list

class SongData:
    def __init__(self, filename):
        self.filename = filename
        self.songs = get_list(self.filename)

    def get_songs(self):
        return list(self.songs.keys())

    def get_lyrics(self, song_artist_pair):
        try:
            return self.songs[song_artist_pair]
        except:
            raise KeyError("Key could not be found")

    def update_songs(self, filename):
        self.filename = filename
        self.songs = get_list(filename)



