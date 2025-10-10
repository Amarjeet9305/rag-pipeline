import io
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_upload_document(client):
    data = {
        'file': (io.BytesIO(b"AI is changing the world."), 'test.txt')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert 'message' in response.json

def test_query_rag(client):
    response = client.post('/query', json={'query': 'What is AI?'})
    assert response.status_code == 200
    assert 'response' in response.json

def test_get_metadata(client):
    response = client.get('/metadata')
    assert response.status_code == 200
    assert isinstance(response.json, dict)
