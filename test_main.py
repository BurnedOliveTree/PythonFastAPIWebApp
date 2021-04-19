from fastapi.testclient import TestClient
import pytest

from main import app

client = TestClient(app)

def test_read_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello world'}

def test_read_method():
    response = client.get('/method')
    assert response.status_code == 200
    assert response.json() == {'method': 'GET'}
    response = client.put('/method')
    assert response.status_code == 200
    assert response.json() == {'method': 'PUT'}
    response = client.options('/method')
    assert response.status_code == 200
    assert response.json() == {'method': 'OPTIONS'}
    response = client.delete('/method')
    assert response.status_code == 200
    assert response.json() == {'method': 'DELETE'}
    response = client.post('/method')
    assert response.status_code == 201
    assert response.json() == {'method': 'POST'}

@pytest.mark.parametrize('name', ['Zenek', 'Marek', 'Alojzy'])
def test_hello_name(name: str):
    response = client.get(f'/hello/{name}')
    assert response.status_code == 200
    assert response.text == f'"Hello {name}"'