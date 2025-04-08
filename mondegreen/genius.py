# pip install lyricsgenius
# https://www.youtube.com/watch?v=CokKFmDnDtw
# https://github.com/johnwmillr/LyricsGenius

import lyricsgenius

genius = lyricsgenius.Genius("79bSVlRX4YEmwomC2oIp_jiWPiGliEtArd2dsIlisD4NfHPPVuRdp-skYhQKmfgn")
# artist = genius.search_artist("Taylor Swift", max_songs=1)
# songs = artist.songs
# for song in songs:
#     print(song.lyrics)

song = genius.search_song("firework", "Katy Perry")
print(song.lyrics)
print(song.song_art_image_thumbnail_url)