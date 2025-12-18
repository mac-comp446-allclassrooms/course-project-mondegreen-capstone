import pytest
from application.lyrics import get_list
from application import create_app
from pathlib import Path

@pytest.fixture()
def client():
    app = create_app("server/application/songs.txt")
    app.config.update({
        "TESTING": True,
    })

    return app.test_client()

def create_tmp_songs(tmp_path,song_content):
    song_file = tmp_path / "songs.txt"
    song_file.write_text(
        song_content
    )
    return get_list(str(song_file))


def test_request_example(client):
    response = client.get("/ping")
    print("RESPONSE DATA:", response.data)
    assert response.status_code == 200
    assert b"pong" in response.data

def test_request_song_list(client):
    response = client.get("/lyrics/list")
    print("RESPONSE DATA:", response.data)
    assert response.status_code == 200

def test_get_list_returns_dict(tmp_path):
    song_content =(
        "Song A:Artist A:Line 1A\n"
        "Song B:Artist B:Line 1B\n"
    )
    songs_dict = create_tmp_songs(tmp_path,song_content)

    assert isinstance(songs_dict, dict)
    assert "Song A:Artist A" in songs_dict
    assert "Song B:Artist B" in songs_dict

    lyrics_a = songs_dict["Song A:Artist A"]
    lyrics_b = songs_dict["Song B:Artist B"]

    assert lyrics_a == "Line 1A\n"
    assert lyrics_b == "Line 1B\n"

def test_get_list_empty_file(tmp_path):
    song_content = ("")
    # song_content = (" ")  # Test is failing here
    songs_dict = create_tmp_songs(tmp_path,song_content)
    assert isinstance(songs_dict, dict)
    assert songs_dict == {}

def test_get_list_single_song(tmp_path):
    song_content = ("Song 1:Artist 1:Some lyrics here\n")
    songs_dict = create_tmp_songs(tmp_path, song_content)
    assert songs_dict == {
        "Song 1:Artist 1": "Some lyrics here\n"
    }

def test_get_list_keeps_whitespace_in_keys(tmp_path):
    song_content = (" Song A : Artist A :Lyrics\n")
    songs_dict = create_tmp_songs(tmp_path,song_content)
    assert " Song A : Artist A " in songs_dict
    assert songs_dict[" Song A : Artist A "] == "Lyrics\n"

def test_get_list_duplicate_keys(tmp_path):
    song_content = (
        "Song A:Artist A:First version\n"
        "Song A:Artist A:Second version\n"
    )
    songs_dict = create_tmp_songs(tmp_path, song_content)
    assert list(songs_dict.keys()) == ["Song A:Artist A"]
    assert songs_dict["Song A:Artist A"] == "Second version\n"

