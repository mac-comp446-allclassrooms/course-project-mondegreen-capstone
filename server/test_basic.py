import pytest
from app import app as flask_app

print("IMPORTING !!!")
@pytest.fixture()
def app():
    flask_app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client():
    return flask_app.test_client()


def test_request_example(client):
    response = client.get("/ping")
    print("RESPONSE DATA:", response.data)
    assert response.status_code == 200
    assert b"pong" in response.data



