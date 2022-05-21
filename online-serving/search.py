from search_modules.tokenization import tokenize_query
from search_modules.pageRank import pagerank

import time
import requests
import json

def get_index_request(tokens, path):
    """
        Retorna la enumeracion encontrada en el index dado un token,
        segun el path especificado.
    """
    r = requests.get('http://localhost:8080/{}?q={}'.format(path, tokens))
    if r.status_code == 200:        
        return r.json()
    else:
        return None

def main(argv):
    """
        Funcion principal
    """

    tokens = tokenize_query(argv)
    if not tokens:
        tokens = argv
    #se obtiene la busqueda de cada token en los indices
    t1 = time.time()
    indexes = get_index_request("+".join(tokens), "st")

    results = None            
    if (indexes):
        ranked_pages = pagerank(indexes)
        t2 = time.time()
        ranked_pages = [{
            "url": ranked_pages[rank]['url'], 
            "title":ranked_pages[rank]['title'], 
            "description":ranked_pages[rank]['description']
        } for rank in ranked_pages]
        results = {
            "status": "success",
            "time": round(t2-t1, 3),
            "results": ranked_pages
        }
    else:
        t2 = time.time()
        results = { "status": 'notfound', "time": round(t2-t1, 3), "results":argv }
    
    return json.dumps(results)
        
if __name__ == "__main__":   
    main("curso test?")
