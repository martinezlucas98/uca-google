from typing import Optional

from fastapi import FastAPI

from expand_query import expand_query 

app = FastAPI()


@app.get("/")
def read_root():
    return {"Google": "++"}

## Soporta parametros como "/expand_query?q=hola%20Google"
@app.get("/expand_query")
def expand_query_route( q: Optional[str] = None):
    
    # if the user send a empty argument
    if not q:
        return {'status': 'empty query'}
        
    
    q = str(q)
    lower_case = q.lower()
    response = expand_query(sentence = lower_case)
    return response



@app.get("/autocomplete")
def autocomplete( q: Optional[str] = None):
    """Given an argument 'q' that will be a string,
    this should return a list of a autocompletes options.

    e.g: 
        q = 'h' -> ['hola', 'hielo', 'hacer']
        q = 'horarios d -> ['horarios de clases', 'horarios de caja', horarios de cantina']
         
    """
    return {"autocompletes": [q + ' example1']} 


