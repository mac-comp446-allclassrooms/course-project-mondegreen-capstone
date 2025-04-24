# pip install lyricsgenius
# https://www.youtube.com/watch?v=CokKFmDnDtw
# https://github.com/johnwmillr/LyricsGenius

import lyricsgenius

genius = lyricsgenius.Genius("79bSVlRX4YEmwomC2oIp_jiWPiGliEtArd2dsIlisD4NfHPPVuRdp-skYhQKmfgn")
# artist = genius.search_artist("Taylor Swift", max_songs=1)
# songs = artist.songs
# for song in songs:
#     print(song.lyrics)

def coverArt(title, artist):
    song = genius.search_song(title, artist)
    return song.song_art_image_thumbnail_url

def getLyrics(title, artist):
    song = genius.search_song(title, artist)
    return song.lyrics

def searchMulti(term):
    results = genius.search(search_term=term, per_page=20, type_='song')
    return results
    

# song = genius.search_song("firework", "Katy Perry")
# print(song.lyrics)
# print(song.song_art_image_thumbnail_url)