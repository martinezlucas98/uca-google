from search_modules.tokenization import tokenize_query
from search_modules.pageRank import pagerank
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

def main(argv):
    """
        Funcion principal
    """
    ex = get_request(PATH_QUERY, "expand_query?q=", "clase test?")
    ex = ex['lemmatized_tokens']

    tokens = tokenize_query(argv)
    if not tokens:
        tokens = argv
    #se obtiene la busqueda de cada token en los indices
    t1 = time.time()
    indexes = get_request(PATH_INDEX, "st?q=", "+".join(tokens))
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
    results = main("curso test?")
    results = json.loads(results)
    
    print(">>>RESULTS:\n")
    print("time:", results['time'], "\n")
    if results['status'] == "success":
        print("Pages:")     
        for item in results['results']:
            print('url:', item['url'])
            print('title:', item['title'])
            print('description:', item['description'], "\n")
    else:
        print("Not found")
        print(results['results'])
