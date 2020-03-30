import pytest


@pytest.fixture
def app():
    from app import app
    return app.test_client()


def test_successful_get(app):
    response = app.get('http://localhost:5000/pokemon/charizard')

    assert response.status_code == 200
    assert response.json['pokemon'] == 'charizard'


def test_not_found_get(app):
    response = app.get('http://localhost:5000/pokemon/charizars')

    assert response.status_code == 404
