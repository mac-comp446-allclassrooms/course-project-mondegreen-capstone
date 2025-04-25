# pip install lyricsgenius
# https://www.youtube.com/watch?v=CokKFmDnDtw
# https://github.com/johnwmillr/LyricsGenius

import re
import string
import lyricsgenius

genius = lyricsgenius.Genius("79bSVlRX4YEmwomC2oIp_jiWPiGliEtArd2dsIlisD4NfHPPVuRdp-skYhQKmfgn", remove_section_headers=False)
# artist = genius.search_artist("Taylor Swift", max_songs=1)
# songs = artist.songs
# for song in songs:
#     print(song.lyrics)

def coverArt(title, artist):
    song = genius.search_song(title, artist)
    return song.song_art_image_thumbnail_url

def clean_lyrics(lyrics):
    song_start = re.search(r'\[.*?\]', lyrics)
    if song_start:
        lyrics = lyrics[song_start.start():]

    lyrics = re.sub(r'\[.*?\]', ' ', lyrics)
    lyrics = lyrics.replace('\n', ' ')
    lyrics = lyrics.replace("'", '')
    lyrics = re.sub(r'''      # used https://stackoverflow.com/questions/34860982/replace-the-punctuation-with-whitespace
               \W+
               \s*
               ''',
               ' ',
               lyrics,
               flags=re.VERBOSE)
    return lyrics


def getLyrics(title, artist):
    song = genius.search_song(title, artist)
    if song:
        return clean_lyrics(song.lyrics)
    return "Lyrics not found"

# song = genius.search_song("firework", "Katy Perry")
# print(song.lyrics)
# print(song.song_art_image_thumbnail_url)