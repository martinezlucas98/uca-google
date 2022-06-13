from typing import Optional

from fastapi import FastAPI

from expand_query import expand_query 
from only_lemma_stemm import only_lemma_stemm
from nlp_tools.autocomplete import autocomplete_gpp
from fastapi.middleware.cors import CORSMiddleware
import datetime

app = FastAPI()


# We need to allow all origins that fetch us. 
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
    expose_headers = ["*"]
)


@app.get("/")
def read_root():
    return {"Google": "++"}

## Soporta parametros como "/expand_query?q=hola%20Google"
@app.get("/expand_query")
def expand_query_route( q: Optional[str] = None):
    """Given an argument 'q' that will be a string,
    this should return a dictionary with attributes
    that will help in the search
    """
    start_time = datetime.datetime.now()
    # if the user send a empty argument
    if not q:
        return {'status': 'empty query'}
        
    
    q = str(q)
    lower_case = q.lower()
    response = expand_query(sentence = lower_case)

    end_time = datetime.datetime.now()
    time_diff = (end_time - start_time)
    execution_time = time_diff.total_seconds() * 1000
    response['execution time'] = execution_time
    return response



@app.get("/autocomplete")
def autocomplete( q: Optional[str] = ''):
    """Given an argument 'q' that will be a string,
    this should return a list of a autocompletes options.

    e.g: 
        q = 'h' -> ['hola', 'hielo', 'hacer']
        q = 'horarios d -> ['horarios de clases', 'horarios de caja', horarios de cantina']
         
    """

    start_time = datetime.datetime.now()

    results = autocomplete_gpp(sentence= q)
    response = {
        'status': 'ok',
        'autocompletes': results
    }
    end_time = datetime.datetime.now()
    time_diff = (end_time - start_time)
    execution_time = time_diff.total_seconds() * 1000
    print("execution time in autocomplete", execution_time, "ms")
    response['execution time'] = execution_time
    print("[autocomplete_response] = ", q, response)

    return response



@app.get("/lemmastemm")
def lemma_and_stemm( q: Optional[str] = ''):
    """
    Do only lemmatization and Steaming to improve perfomance
    """
    
    start_time = datetime.datetime.now()
    q = str(q)
    lower_case = q.lower()

    response = only_lemma_stemm(sentence = lower_case)

    end_time = datetime.datetime.now()
    time_diff = (end_time - start_time)
    execution_time = time_diff.total_seconds() * 1000
    response['execution time'] = execution_time

    return response




