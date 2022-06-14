import math
import numpy as np

class TfIdf:
    """
        Implementacion del modelo matematico TF-IDF (term frecuency and inverse document frequency),
        para medir la importancia de un documento/pagina.

        *Artibutos:
            @tokens: dict{'token':{'page_id1': int, 'page2':int,...}, ...}
                por cada token se identifica las paginas en las que aperece, y cada pagina tiene
                asociado un valor entero que es frecuencia en la que aparece en una pagina.
            @pages: dict{'page_id':{'url':str, 'title':str, 'description':str, 'content':str},...}
                contiene el total de paginas donde aparecen los tokens,
                donde cada id del diccionario representa otro dict que contiene la informacion de
                la pagina.
            @indexes_tf_idf: list[tuple(int,float),...]
                contiene una lista de tuplas, list[(page_id1, score1), (page_id2, score2), ...], donde
                page_id es el identificador asociada a su score.
    """  
    def __init__(self, indexes):
        self.__tokens = indexes['tokens']
        self.__pages = indexes['pages']
        self.__indexes_tf_idf = []
             
    def term_frequency(self, token, page_id):
        """
        *Description:
            Se calcula la frecuncia de ocurrencia de un token/termino en una pagina con identificador 'page_id'.
        *Parameters
            @token: str
                Un token correspondiente de self.__tokens.
            @page_id: int
                Identificador de la pagina/documento actual.
        *Returns        
            @tf: float
                Frecuencia de ocurrencia de token en el pagina __pages[page_id]
        """

        # si el __token[token] no tiene asociado un key page_id, significa que 
        # no hay ocurrencia del token con una pagina con identificador page_id
        freq = 0
        try:
            # __tokens es un dict{token1: dict{page_id1:count1}, token2: dict{page_id2:count2}, ...}
            freq = self.__tokens[token][page_id]
        except Exception as err:
            pass        
        # verificamos si el titulo esta vacio (None)
        title = self.__pages[page_id]['title']
        if not title:
            title = ""    
        # calculamos la longitud del contenido total de la pagina
        title = title.split(' ')
        content = self.__pages[page_id]['content']
        content_len = len(title) + len(content)
        # se devuelve la frecuencia del termino (tf)
        return freq / content_len

    def inverse_document_frequency(self, token):
        """
        *Description:
            Calcula la frecuencia de ocurrencia del token en la colección de documentos/paginas,
            para medir que tan relevante es una palabra/token en una coleccion de documentos/paginas.
        *Parameters
            @token : str
                El token correspondiente como identificador.
        *Returns
            @idf: float
                El calculo idf del token.
        """
        # el numero de documentos/paginas en el cual aparece el token (document frequency)
        df = len(self.__tokens[token])
        # el numero total de paginas
        N = len(self.__pages.keys())        
        return np.log10(N / (df + 1))


    def get_results (self):
        """
        *Description:
            Se obtiene el resultado actual de __indexes_tf_idf con los datos de 
            url, title y descripcion de cada pagina.
        *Parameters
            @self
        *Returns
            @results: list[dict{'url':str, 'title':str, 'description':str}]
                Cada diccionario en la lista representa una pagina, y cada elemento
                del diccionario representa el contenido de la pagina.
        """
        results = []
        # cada item es una tupla (page_id, score)
        for item in self.__indexes_tf_idf:
            page_id = item[0]
            description = self.__pages[page_id]['content']
            description = description[:300]         
            results.append(
                {
                    "url": self.__pages[page_id]['url'],
                    "title": self.__pages[page_id]['title'],
                    "description": description
                }
            )
        return results

    def sort(self):
        """
            Ordena el contenido del resultado por relevancia, en orden decreciente.
        """
        # __indexes_tf_idf representa una lista de tuplas, list[(page_id1, score1), (page_id2, score2), ...]
        self.__indexes_tf_idf = sorted(self.__indexes_tf_idf, key=lambda x: x[1], reverse=True)

    def rank_pages(self):
        """
        *Description:
            Puntua cada pagina obtenida del indexs para medir que tan relevante son
            cada paginas. Se aplica el metodo numerico tf-idf(t,d) = tf(t,d) * idf(t)
        *Parameters
            @self
        *Returns
            @None
        """
        # cada page_id es el identicador de cada pagina
        for page_id in self.__pages:
            score = 0.0
            # hacemos el split para poder puntuar el correctamente el contenido de la pagina para cada token            
            self.__pages[page_id]['content'] = self.__pages[page_id]['content'].split(' ')
            for token in self.__tokens:
                # calculamos la frecuencia de ocurrencia del token en el contenido de la pagina con id page_id
                tf = self.term_frequency(token, page_id)
                # calculamos la frecuencia de ocurrencia del token en todas las paginas
                idf = self.inverse_document_frequency(token)
                # aplicamos la formula de tf-idf = tf*idf para la puntuacion, y sumamos a cada puntuacion
                score += tf * idf
            self.__indexes_tf_idf.append((page_id, score))
            