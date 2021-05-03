from fastapi.testclient import TestClient
from datetime import date, timedelta
import pytest

from main import app

client = TestClient(app)

def test_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello world!'}

def test_method():
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

def test_hello():
    response = client.get(f'/hello/')
    assert response.status_code == 200
    assert response.content.decode('utf-8') == f'<h1>Hello! Today date is {date.today()}</h1>'

# @pytest.mark.parametrize('name', ['Zenek', 'Marek', 'Alojzy'])
# def test_hello_name(name: str):
#     response = client.get(f'/hello/{name}')
#     assert response.status_code == 200
#     assert response.text == f'"Hello {name}"'

def test_auth():
    response = client.get('/auth?password=haslo&password_hash=013c6889f799cd986a735118e1888727d1435f7f623d05d58c61bf2cd8b49ac90105e5786ceaabd62bbc27336153d0d316b2d13b36804080c44aa6198c533215')
    assert response.status_code == 204
    response = client.get('/auth?password=haslo&password_hash=f34ad4b3ae1e2cf33092e2abb60dc0444781c15d0e2e9ecdb37e4b14176a0164027b05900e09fa0f61a1882e0b89fbfa5dcfcc9765dd2ca4377e2c794837e091')
    assert response.status_code == 401

def test_register():
    response = client.post('/register', json={"name": "Jan", "surname": "Nowak"})
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "Jan",
        "surname": "Nowak",
        "register_date": str(date.today()),
        "vaccination_date": str(date.today() + timedelta(days=8))
    }

def test_patient():
    response = client.get('/patient/1')
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Jan",
        "surname": "Nowak",
        "register_date": str(date.today()),
        "vaccination_date": str(date.today() + timedelta(days=8))
    }
    response = client.get('/patient/20')
    assert response.status_code == 404
    response = client.get('/patient/0')
    assert response.status_code == 400