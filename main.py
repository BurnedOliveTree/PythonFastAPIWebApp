from fastapi import FastAPI, Request

app = FastAPI()

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