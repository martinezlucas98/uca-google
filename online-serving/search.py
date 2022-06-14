from search_modules.tokenization import tokenize_query
from search_modules.pageRank import PageRank
from search_modules.tf_idf import TfIdf
from search_modules.bm25 import BM25
from settings import PATH_INDEX, PATH_QUERY

import time
import requests
import json

def get_request(path, query_path, argv):
    """
    *Description:
        Request con el metodo GET, para los servicios index y query-understanding.
    *Parameters
            @path: str
                ruta absoluta del servicio, ej: http://localhost:8080/
            @query_path: str
                ruta del tipo de servicio en cuestion, ej: st?q=
            @argv: str
                el valor del argumento, ej: universidad+catolica
    *Returns
        @r: json
            el json de la respuesta obtenida.
    """
    r = requests.get(path + query_path + argv)
    if r.status_code == 200:
        # return r
        return r.json()
    else:
        return None

def ranking_function(Obj):
    """
        *Description:
            Funcion que se encarga de ejecutar los diferentes algoritmos de rankeo de paginas.
        *Parameters
            @Obj: object
                Es un objeto generico que se encarga de ejectuar los metodos correspondientes de 
                la instancia recibida.
        *Returns
            @rankes_pages: list[dict{'url':str, 'title':str, 'description':str}]
            Cada diccionario en la lista representa una pagina, y cada elemento
            del diccionario representa el contenido de la pagina.
        """ 
    Obj.rank_pages()
    Obj.sort()
    ranked_pages = Obj.get_results()
    return ranked_pages

def search(argv):
    """
    *Description:
        Funcion principal que ejecuta los algoritmos de busquedas.
    *Parameters:
        @argv: str
            La palabra sin tokenizar a buscar.
    *Returns:
        @None
    """
    t1 = time.time()
    #tokenizamos el query
    tokens = get_request(PATH_QUERY, "lemmastemm?q=",argv)
    query_tokens = tokens['stemmed_tokens']
    #si esta vacio, significa que solo tenemos stopwords
    if not bool(query_tokens):
        query_tokens = tokens['corrected_sentence'].split(' ')
    #se obtiene la busqueda de cada token en los indices
    indexes = get_request(PATH_INDEX, "st?q=", "+".join(query_tokens))
    results = None
    # si el inidice no esta vacio signfica que hay resultados a rankear
    if (len(indexes['pages'].keys())):
        # obj = PageRank(indexes)
        # obj = TfIdf(indexes)
        obj = BM25(indexes)

        ranked_pages = ranking_function(obj)
        t2 = time.time()
        results = { "status": "success", "time": round(t2-t1, 3), "results": ranked_pages }
    else:
        t2 = time.time()
        results = { "status": 'notfound', "time": round(t2-t1, 3), "results":argv }
    
    return json.dumps(results)

if __name__ == "__main__":
    sentence = "ingenieria en informatica"
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
