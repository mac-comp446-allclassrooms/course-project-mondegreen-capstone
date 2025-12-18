import string
import unicodedata
from typing_extensions import deprecated


@deprecated("Lyrics currently live in the dict in app")
def get_lyrics(title, artist, file):
    with open(file, "r") as songs:
        songs = songs.readlines()
        for i in range(len(songs)):
            split = songs[i].split(":")
            if split[0].lower() == title and split[1].lower() == artist:
                return split[2]

def get_list(file):
    with open(file, "r") as songs:
        songs = songs.readlines()
        out = {}
        for i in range(len(songs)):
            split = songs[i].split(":")
            out[str(split[0])+":"+str(split[1])]=split[2]
        return out