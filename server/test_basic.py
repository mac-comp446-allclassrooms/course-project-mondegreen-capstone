import pytest
from server import create_app

@pytest.fixture()
def client():
    app = create_app("server/songs.txt")
    app.config.update({
        "TESTING": True,
    })

    return app.test_client()


def test_request_example(client):
    response = client.get("/ping")
    print("RESPONSE DATA:", response.data)
    assert response.status_code == 200
    assert b"pong" in response.data

def test_request_song_list(client):
    response = client.get("/lyrics/list")
    print("RESPONSE DATA:", response.data)
    assert response.status_code == 200



