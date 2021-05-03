from fastapi import FastAPI, Request, Response, Depends, Cookie
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from hashlib import sha512
from pydantic import BaseModel
from datetime import date, timedelta
import re

app = FastAPI()
app.counter = 0
app.patients = dict()
security = HTTPBasic()

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

@app.get('/hello')
def hello():
    return HTMLResponse(content=f'<h1>Hello! Today date is {date.today()}</h1>')

@app.post('/login_session')
def login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == '4dm1n' and credentials.password == 'NotSoSecurePa$$':
        response.status_code = 201
        app.counter += 1
        response.set_cookie(key="session_token", value=app.counter)
    else:
        response.status_code = 401
    return response
    
@app.post('/login_token')
def login_token(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == '4dm1n' and credentials.password == 'NotSoSecurePa$$':
        response.status_code = 201
        return {'token': app.counter}
    else:
        response.status_code = 401

# @app.get('/hello/{name}')
# def hello_name_view(name: str):
#     return f'Hello {name}'

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
def register(patient: Patient):
    app.counter += 1
    patient.id = app.counter
    patient.register_date = str(date.today())
    patient.vaccination_date = str(date.today() + timedelta(days=len(re.sub("[^a-zA-Z]+", '', patient.name+patient.surname))))
    app.patients[app.counter] = patient
    return patient

@app.get("/patient/{id}")
def patient(response: Response, id: int):
    if id < 1:
        response.status_code = 400
    elif id not in app.patients.keys():
        response.status_code = 404
    else:
        response.status_code = 200
        return app.patients[id]
    