from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Google": "++"}

## Soporta parametros como "/expand_query?q=hola%20Google"
@app.get("/expand_query")
def read_item( q: Optional[str] = None):
    return {"q o parametro": q}