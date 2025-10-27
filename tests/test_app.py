import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200

def test_about(client):
    rv = client.get('/about')
    assert rv.status_code == 200

def test_contact(client):
    rv = client.get('/contact')
    assert rv.status_code == 200
