# pip install lyricsgenius
# https://www.youtube.com/watch?v=CokKFmDnDtw
# https://github.com/johnwmillr/LyricsGenius

# if you're reading this, henry was able to push a commit!

import re
import string
import lyricsgenius
import unicodedata

genius = lyricsgenius.Genius("79bSVlRX4YEmwomC2oIp_jiWPiGliEtArd2dsIlisD4NfHPPVuRdp-skYhQKmfgn", remove_section_headers=False)
# artist = genius.search_artist("Taylor Swift", max_songs=1)
# songs = artist.songs
# for song in songs:
#     print(song.lyrics)

def coverArt(title, artist):
    song = genius.search_song(title, artist)
    return song.song_art_image_thumbnail_url

def clean_lyrics(lyrics):
    lyrics = unicodedata.normalize("NFKD", lyrics)
    song_start_brackets = re.search(r'\[.*?\]', lyrics)
    if song_start_brackets:
        lyrics = lyrics[song_start_brackets.start():]
    else:
        song_start_else = list(re.finditer(r'\.[^\s\'"]', lyrics))
        if len(song_start_else) >= 2:
            lyrics = lyrics[song_start_else[len(song_start_else)-1].start():]
        elif song_start_else:
            lyrics = lyrics[song_start_else[0].start():]
    
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
    return lyrics.lower()


def getLyrics(title, artist):
    song = genius.search_song(title, artist)
    if song:
        print(song.lyrics)
        return clean_lyrics(song.lyrics)
        # return song.lyrics
    return "Lyrics not found"

def searchMulti(term):
    data = genius.search(search_term=term, per_page=9, type_='song')

    songs = []

    for section in data.get('sections', []):

        if section.get('type') == 'song':

            for hit in section.get('hits', []):

                result = hit.get('result', {})

    # Extract fields here

                song_data = {

                'title': result.get('title'),

                'artist': result.get('artist_names'),

                'release_date': result.get('release_date_for_display', 'N/A'),

                'url': result.get('url'),

                'song_art_image_thumbnail_url': result.get('song_art_image_thumbnail_url'),

                'pageviews': result.get('stats', {}).get('pageviews', 0),

                'annotations': result.get('annotation_count', 0)

                }

                songs.append(song_data)

    results = []
    # Print the results
    for song in songs:
        results.append(f"Title: {song['title']}, Artist: {song['artist']}, Release Date: {song['release_date']}, URL: {song['url']}, Pageviews: {song['pageviews']}, ImageURL: {song['song_art_image_thumbnail_url']}")
    return songs

# Not implemented
# def searchGenre(genre):
#     print('Genre: ', genre)
#     data = genius.tag(name = genre)
#     if genre == 'r-b':
#         data = genius.tag(name =  'r-b')
#     print("Genre data: ", data)

#     results = []
#     songs = data['hits']

#     for song in songs:
#         song_data = {
#         'title' : song['title'],
#         'artist' : song['artists'][0]
#         }

#         results.append(song_data)

#     return results

def getCover(title, artist):
    song = genius.search_song(title, artist)
    if song:
        return song.song_art_image_thumbnail_url
    return "Cover not found"