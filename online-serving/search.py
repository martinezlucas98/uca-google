import json
import requests
import time
#modulos para tokenizar
import string
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

#ajustar a python 3.9.2 en requerimientos

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
    # print(dict(Counter(query_tokens)))

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
    # @ToDo: funcion que rankea estos resultados
    t2 = time.time()

    #@rem: mostramos resultados (borrar luego)
    print("tiempo:", round(t2-t1, 3))
    if (indexes):
        indexes_keys = list(indexes.keys())
        for tk in indexes_keys:
            print(tk)
            for item in indexes[tk]:
                print("{}   {}".format(item['url'], item['count']))
            print()
    else:
        results = { "status": 'notfound', "time": round(t2-t1, 3), "results":argv }
        print(results)
        #return results 

        
if __name__ == "__main__":   
    main("¿Quien creo los testing?")
