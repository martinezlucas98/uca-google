
"""
*todo:
    @search(argv)
        Se encarga de ejecutar los algoritmos de busquedas, primero tokeniza la palabra en donde
        puede existir tokens con el mismo significado, una manera de reforzar las puntuaciones
        es identificar estos tokens para poder contar el numero de ocurrencia de cada tokens en
        la palabra y agregar un peso a las puntuaciones.
        Ej:
            "Carrera de informatica y carrera de electronica"
            tokens = ['carrer', 'inform', 'carrer', 'electro']
            Y poder identificarlos asi:
            tokens = {'carrer':2, 'inform':1, 'electro':1}
        Problemas?
            "informacion acerca de las carreras de informatica y electronica"
            tokens = ['inform', 'carrer', 'inform', 'electro']
            tokens = {'inform': 2, 'carrer': 1, 'electro': 1}
            Podemos observar que informacion e infomatica nos referimos a lo mismo, por lo que
            podemos no obtener nada con relacion a electronica.
"""

# modulos del servicio
from search_modules.tokenization import tokenize_query
from search_modules.pageRank import GraphPageRank
from search_modules.tf_idf import TfIdf
from search_modules.bm25 import BM25
from settings import PATH_INDEX, PATH_QUERY
# modulos python
import time
import requests
import json
from optparse import OptionParser

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
            Funcion que se encarga de ejecutar los algoritmos tf_idf y BM25.
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

def pageRank_function(pages):
    """
        *Description:
            Se encarga de rankear las paginas con el algoritmo pageRank.
        *Parameters
           @pages: dict{'page_id':{'url':str, 'title':str, 'description':str, 'content':str},...}
                contiene el total de paginas donde aparecen los tokens,
                donde cada id del diccionario representa otro dict que contiene la informacion de
                la pagina.
        *Returns
            @rankes_pages: list[dict{'url':str, 'title':str, 'description':str}]
            Cada diccionario en la lista representa una pagina, y cada elemento
            del diccionario representa el contenido de la pagina.
        """ 
    page_rank = GraphPageRank()
    page_rank.init(pages)
    page_rank.pagerank()
    page_rank.sort()
    ranked_pages = page_rank.get_results(pages)
    return ranked_pages

def search(sentence, type='bm25'):
    """
    *Description:
        Funcion principal que ejecuta los algoritmos de busquedas.
    *Parameters:
        @sentence: str 
            La palabra sin tokenizar a buscar, posibles valores bm25|pgrk|tfidf
        @type: str 
            El tipo de algoritmo de busqueda a ejecutar
    *Returns:
        @None
    """
    t1 = time.time()
    #tokenizamos el query
    tokens = get_request(PATH_QUERY, "lemmastemm?q=",sentence)
    query_tokens = tokens['stemmed_tokens']
    #si esta vacio, significa que solo tenemos stopwords
    if not bool(query_tokens):
        query_tokens = tokens['corrected_sentence'].split(' ')
    #se obtiene la busqueda de cada token en los indices
    indexes = get_request(PATH_INDEX, "st?q=", "+".join(query_tokens))
    results = None
    # si el inidice no esta vacio signfica que hay resultados a rankear
    if (len(indexes['pages'].keys())):
        ranked_pages = None
        # ejecutamos uno de los algoritmos de busqueda
        if type == 'bm25':
            ranked_pages = ranking_function(BM25(indexes))
        elif type == 'pgrk':
            ranked_pages = pageRank_function(indexes['pages'])
        else:
            ranked_pages = ranking_function(TfIdf(indexes))

        t2 = time.time()
        results = { "status": "success", "time": round(t2-t1, 3), "results": ranked_pages }
    else:
        t2 = time.time()
        results = { "status": 'notfound', "time": round(t2-t1, 3), "results":sentence }
    
    return json.dumps(results)

def display(sentence, type, ranking):
    """
    *Description:
        Muestra en consola los resultados de busqueda de acuerdo al ranking especificado.
    *Parameters:
        @sentence: str 
            La palabra sin tokenizar a buscar, posibles valores bm25|pgrk|tfidf
        @type: str 
            El tipo de algoritmo de busqueda a ejecutar
        @ranking: int
            El numero de paginas a mostrar.
    *Returns
        None
    """
    results = search(sentence, type)
    results = json.loads(results)
    print(f"\tSearch:  {sentence}\n")
    print("Type:", type, '\n')
    print(">>>RESULTS:\n")
    print('Resultados encontrados: ', len(results['results']), 'paginas')
    print("time:", results['time'], "\n")
    if results['status'] == "success":
        print("Las",ranking,"primeras paginas:")
        count = 0
        for item in results['results']:
            print('\turl:', item['url'])
            print('\ttitle:', item['title'])
            print('\tdescription:', item['description'][:100] + "...", "\n")
            count += 1
            if count == ranking:
                break
    else:
        print("Not found:", results['results'])

if __name__ == "__main__":
    usage = "usage: %prog [-a] <bm25|pgrk|tfidf> [-s] <str1+st2+strN> [-r] <n-pages>"
    optparser = OptionParser(usage=usage)
    optparser.add_option('-a', '--algorithm',
                         action='store',
                         dest='algorithm',
                         help='type of search algorithm, type:string, values=bm25|pgrk|tfidf',
                         default='bm25',
                         type='string')
    optparser.add_option('-s', '--sentence',
                         dest='sentence',
                         help='search sentence, type: string, values=str1+st2+strN',
                         default="universidad+catolica",
                         type='string')
    optparser.add_option('-r', '--ranking',
                         dest='ranking',
                         help='ranking pages, type: int, value=10 [default]',
                         default=10,
                         type='int')
    (options, args) = optparser.parse_args()

    # obtenemos los valores de las opciones
    sentence = options.sentence
    algorithm = options.algorithm
    ranking = options.ranking
    # verificamos el formato
    if len(args) >=1:
        optparser.error("incorrect number of arguments")
    if algorithm != 'bm25' and algorithm != 'pgrk' and algorithm != 'tfidf':
        optparser.error("incorrect values, for [-a] values=bm25|pgrk|tfidf")
    
    # realizamos la busqueda
    sentence = sentence.replace("+", " ")
    display(sentence, algorithm, ranking)
