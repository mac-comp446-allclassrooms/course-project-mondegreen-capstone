# pip install lyricsgenius
# https://www.youtube.com/watch?v=CokKFmDnDtw
# https://github.com/johnwmillr/LyricsGenius

import lyricsgenius

genius = lyricsgenius.Genius("vhYwxFqXZyHroY1Ctj1er8YNSQP6SEWT2B8GfZgVT6Rdu0Q-ZYoysfmCFf8JozBq")
# artist = genius.search_artist("Taylor Swift", max_songs=1)
# songs = artist.songs
# for song in songs:
#     print(song.lyrics)

song = genius.search_song("firework", "Katy Perry")
print(song.lyrics)
print(song.song_art_image_thumbnail_url)