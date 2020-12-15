"""server"""
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    """Index view"""
    return 'Hello world'
