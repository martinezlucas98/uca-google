from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.get("/")
def read_root():
    return {"welcome": "online serving"}

@app.get("/search")
def search(q: Optional[str] = None):
    """
        Devuelve los datos de busqueda por relevancia.
    """
    #data = get_
    data = {
        "status": "success",
        "time": 0.8,
        "results": [
            {
                "title": "Algun titulo del html",
                "url": 'https://name.com'
            },
            {
                "title": "Algun titulo del html",
                "url": 'https://www.name2.com'
            },
            {
            "title": "Algun titulo del html",
                "url": 'https://www.nameN.com'
            }
        ]           
    }
    return data