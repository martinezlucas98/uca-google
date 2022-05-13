import json
import requests
import time
import numpy as np
import random
import json
#modulos para tokenizar
import string
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

#probabilidad en el que se salta a unos de los links (para el pageRank)
DAMPING_FACTOR = 0.85

def get_index_request(token, path):
    """
        Retorna la enumeracion encontrada en el index dado un token,
        segun el path especificado.
    """
    r = requests.get('http://localhost:8080/{}?q={}'.format(path, token))
    if r.status_code == 200:        
        return r.json()
    else:
        return None

def tokenize_query(query: str):
    """
        Retorna el query tokenizado.
        Ej:
        query = "¿Donde queda ubicado Paraguay?"
        return ['queda', 'ubicado', 'paraguay']
    """
    STOP_WORDS = stopwords.words('spanish')
    query_tokens = word_tokenize(query)
    query_tokens = [tk.lower() for tk in query_tokens]

    # eliminar los signos de puntuacion (?,?,!,(),#,etc) de cada token
    re_punc = re.compile('[%s]' % re.escape(string.punctuation))
    query_tokens = [re_punc.sub('', tk) for tk in query_tokens]
    query_tokens = [tk for tk in query_tokens if tk.isalpha()]

    #eliminar los stop words
    query_tokens = [tk for tk in query_tokens if tk not in STOP_WORDS]
    
    #contamos la ocurrencia de cada token
    return query_tokens

def generate_pages_linked(indexes):
    """
        Generamos los enlaces entre las paginas de manera aleatoria 
        para la pruebas  el algoritmo pageRank, devuelve un dict con la pagina 
        como key y como valor una lista con las paginas enlazadas.
    """
    #se genera el dict
    indexes_keys = list(indexes.keys())
    linked_pages = {}
    for tk in indexes_keys:
        for item in indexes[tk]:
            linked_pages[item['url']] = []

    #enlazamos las paginas de manera aleatoria    
    pages_keys = list(linked_pages.keys())
    for page in linked_pages:
        links = random.randint(1, len(linked_pages.keys()))
        visited = []
        visited.append(page)
        while links > 0:
            link = random.choice(pages_keys)
            if (link not in visited):
                    linked_pages[page].append(link)
                    visited.append(link)
            links -= 1
        if not linked_pages[page]:
            linked_pages[page].append(pages_keys[pages_keys.index(page)-1])   
    return linked_pages      
    
def pagerank(indexes_pages, n=1000):
    """
        Retorna un diccionario donde las keys son las paginas asociado
        con valor de rankeo de pageRank, n es n-iteraciones suficientes para poder 
        converger los valores rankeados. 
    """
    indexes_pages = generate_pages_linked(indexes_pages)
    # comenzamos en una pagina aleatoria
    page = random.choice(list(indexes_pages.keys()))
    # contendra todas las posibles paginas a visitar a partir de la pag. actual
    # para luego poder rankear.
    visited = []
    visited.append(page)
    
    # agregamos a visitados todas las posibles paginas que visitaremos a partir de la actual
    # logicamente habra mas de uno.
    for i in range(n):        
        probabilities = get_next_page_prob(indexes_pages, visited[i])
        next_page = np.random.choice(list(probabilities.keys()), p=list(probabilities.values()))
        # agregamos la siguiente pagina posible a visitar
        visited.append(next_page)
    
    #rankeamos las paginas
    ranked_pages = {}
    for page in indexes_pages.keys():
        ranked_pages[page] = visited.count(page)/len(visited)
    return ranked_pages

def get_next_page_prob(indexes_pages, current_page):
    """
        Retorna una distribución de probabilidad sobre qué página visitar a continuación,
        a partir de la pagina actual, donde el key es la pagina y el valor es la probabilidad
        de que sea la siguiente pagina a visitar.
    """
    # calculamos la prob. de visitar cualquier otra pagina aleatoria, si la pagina actual no tiene
    # links a otras paginas directamente sabemos que se visitara cualquier otra pagina en caso contrario
    # debemos saber que tan probable es visitar una pagina mediante links enlazados o ir directamente
    # a otra pagina (sin links).
    probability = {}
    if len(indexes_pages[current_page]) == 0:
        #si no tenemos ningun otro link se visita cualquier otra pagina
        prob_page = 1/len(indexes_pages.keys())
    else:
        #prob. de cuando se visita directamente otra pagina (sin los links)
        prob_page = (1-DAMPING_FACTOR)/len(indexes_pages.keys())
        #prob. de seguir visitando paginas mediante los links
        prob_link = DAMPING_FACTOR/len(indexes_pages[current_page])

    #cargamos una distribucion de posibilidades de que pagina visitar de todas las posibles        
    for page in indexes_pages.keys():
        if page in indexes_pages[current_page]:
            probability[page] = prob_page + prob_link
        else:
            probability[page] = prob_page
                                                
    return probability   


def main(argv):
    """
        Funcion principal
    """

    tokens = tokenize_query(argv)
    #se obtiene la busqueda de cada token en los indices
    t1 = time.time()
    indexes = get_index_request(tokens[0], "st")    
    for i in range(1, len(tokens)):        
        indexes.update(get_index_request(tokens[i], "st"))

    results = None            
    if (indexes):
        ranked_pages = pagerank(indexes)
        ranked_pages = sorted(ranked_pages)
        t2 = time.time()
        ranked_pages = [{"url": page} for page in ranked_pages]
        print()
        print(ranked_pages)
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
    main("¿Quien creo los testing?")
