from fastapi import FastAPI
from typing import Optional
from search import main

app = FastAPI()

@app.get("/")
def read_root():
    return {"welcome": "online serving"}

@app.get("/search")
def search(q: Optional[str] = None):
    """
        Devuelve los datos de busqueda por relevancia.
    """
    data = main(str(q))
    return data