import string
import unicodedata

def getLyrics(title, artist):
    with open("songs.txt", "r") as songs:
        songs = songs.readlines()
        for i in range(len(songs)):
            split = songs[i].split(":")
            if split[0].lower() == title and split[1].lower() == artist:
                return split[2]

def getList():
    with open("songs.txt", "r") as songs:
        songs = songs.readlines()
        out = []
        for i in range(len(songs)):
            split = songs[i].split(":")
            out.append(str(split[0])+":"+str(split[1]))
        return out