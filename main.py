from fastapi import FastAPI, Request, Response
from hashlib import sha512
from pydantic import BaseModel
from datetime import date, timedelta
import re

app = FastAPI()
app.counter = 0

class Patient(BaseModel):
    id: int = None
    name: str
    surname: str
    register_date: str = None
    vaccination_date: str = None

@app.get('/')
def root():
    return {'message': 'Hello world!'}

@app.get('/method')
@app.put('/method')
@app.options('/method')
@app.delete('/method')
@app.post('/method', status_code=201)
def method(request: Request):
    return {'method': request.method}

@app.get('/hello/{name}')
def hello_name_view(name: str):
    return f'Hello {name}'

@app.get('/auth')
def auth(response: Response, password: str = None, password_hash: str = None):
    if password is None or password_hash is None or len(password) == 0 or len(password_hash) == 0:
        response.status_code = 401
    else:
        if sha512(password.encode('utf-8')).hexdigest() == password_hash:
            response.status_code = 204
        else:
            response.status_code = 401

@app.post("/register", status_code=201)
async def register(patient: Patient):
    app.counter += 1
    patient.id = app.counter
    patient.register_date = str(date.today())
    patient.vaccination_date = str(date.today() + timedelta(days=len(re.sub("[^a-zA-Z]+", '', patient.name+patient.surname)))
    return patient