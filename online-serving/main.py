from fastapi import FastAPI
from typing import Optional
from search import search

app = FastAPI()

@app.get("/")
def read_root():
    return {"welcome": "online serving"}

@app.get("/search")
def search_service(q: Optional[str] = None):
    """
        Devuelve los datos de busqueda por relevancia.
    """
    data = search(str(q))
    return data