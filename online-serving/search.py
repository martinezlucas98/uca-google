from search_modules.tokenization import tokenize_query
from search_modules.pageRank import pagerank, generate_pages
from settings import PATH_INDEX, PATH_QUERY

import time
import requests
import json

def get_request(path, query_path, argv):
    """
        Request con el metodo GET de alguno de los microsevicios(index o query-understanding).
    """
    r = requests.get(path + query_path + argv)
    if r.status_code == 200:        
        return r.json()
    else:
        return None

def search(argv):
    """
        Funcion principal
    """
    #tokenizamos el query
    tokens = get_request(PATH_QUERY, "expand_query?q=",argv)
    query_tokens = tokens['stemmed_tokens']
    
    if not bool(query_tokens):
        query_tokens = tokens['corrected_sentence'].split(' ')
    #se obtiene la busqueda de cada token en los indices
    t1 = time.time()
    indexes = get_request(PATH_INDEX, "st?q=", "+".join(query_tokens))
    results = None            
    if (indexes):
        # generamos los backlinks correctos y obtenemos la puntuacion de c/pag con pageRank
        indexes = generate_pages(indexes)
        ranked_pages = pagerank(indexes)
        #odernamos de acuerdo a la puntuacion
        ranked_pages= dict(sorted(ranked_pages.items(), key=lambda x: x[1], reverse=True))
        t2 = time.time()        
        ranked_pages = [{
                "url": page, 
                "title":indexes[page]['title'], 
                "description":indexes[page]['description']
        } for page in ranked_pages.keys()]
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
    sentence = "que se estudia en la carrera de ingenieria en informatica?" 
    results = search(sentence)
    results = json.loads(results)
    print(f"\tSearch:  {sentence}\n")
    print(">>>RESULTS:\n")
    print("time:", results['time'], "\n")
    if results['status'] == "success":
        print("Pages:")     
        for item in results['results']:
            print('\turl:', item['url'])
            print('\ttitle:', item['title'])
            print('\tdescription:', item['description'], "\n")
    else:
        print("Not found:", results['results'])
