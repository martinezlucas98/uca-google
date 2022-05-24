from fastapi import FastAPI
from typing import Optional
from search import search
import json

app = FastAPI()

@app.get("/")
def read_root():
    return {"welcome": "online serving"}

@app.get("/search")
def search_service(q: Optional[str] = None):
    """
        Devuelve los datos de busqueda por relevancia.
    """
    q = str(q)
    if (q == ""):
        results = { "status": 'notfound', "time": 0.0, "results":q }
        return json.dumps(results)
        
    data = search(str(q))
    return data