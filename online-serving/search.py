from search_modules.tokenization import tokenize_query
from search_modules.pageRank import PageRank
from search_modules.tf_idf import TfIdf
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
        # return r
        return r.json()
    else:
        return None

def pageRank(indexes):
    t1 = time.time()
    page_rank = PageRank(indexes)
    page_rank.pagerank()
    page_rank.sort()
    ranked_pages = page_rank.get_results()
    t2 = time.time()
    results = {
        "status": "success",
        "time": round(t2-t1, 3),
        "results": ranked_pages
    }
    return results

def tf_idf(indexes):
    t1 = time.time()
    tf_idf = TfIdf(indexes)
    tf_idf.rank_pages()
    tf_idf.sort()
    ranked_pages = tf_idf.get_results()
    t2 = time.time()
    results = {
        "status": "success",
        "time": round(t2-t1, 3),
        "results": ranked_pages
    }
    return results

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
        # results =  pageRank(indexes)        
        results = tf_idf(indexes)
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
    print('Resultados encontrados: ', len(results['results']), 'paginas')
    print("time:", results['time'], "\n")
    if results['status'] == "success":
        print("Las 10 primeras paginas:")
        count = 0
        for item in results['results']:
            print('\turl:', item['url'])
            print('\ttitle:', item['title'])
            print('\tdescription:', item['description'], "\n")
            count += 1
            if count == 10:
                break
    else:
        print("Not found:", results['results'])
