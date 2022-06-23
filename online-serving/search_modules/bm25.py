
import numpy as np
class BM25():
    """
        Implementacion de la funcion de ranking Best matching 25 (BM25).

        *Artibutos:
            @tokens: dict{'token':{'page_id1': int, 'page2':int,...}, ...}
                por cada token se identifica las paginas en las que aperece, y cada pagina tiene
                asociado un valor entero que es frecuencia en la que aparece en una pagina.
            @pages: dict{'page_id':{'url':str, 'title':str, 'description':str, 'content':str},...}
                contiene el total de paginas donde aparecen los tokens,
                donde cada id del diccionario representa otro dict que contiene la informacion de
                la pagina.
            @indexes_bm25: list[tuple(int,float),...]
                contiene una lista de tuplas, list[(page_id1, score1), (page_id2, score2), ...], donde
                page_id es el identificador asociada a su score.
            @k: float
                parametro de "suavizacion" libre para BM25.
            @b: float
                parametro de "suavizacion" libre para BM25.
            @epsilon: float
                constante usada para las paginas con idf negativo.
            @content_len: dict{'page_id':int,...}
                cada page_id contiene la longitud total del contenido de la pagina.            
            @avgdl: float
                Average length del total de paginas.
            @token_idfs: dict{'token':float, ...}
                cada token contiene el calculo su idf.
    """  
    def __init__(self, indexes, k=1.5, b=0.75, e=0.25):
        self.__tokens = indexes['tokens']
        self.__pages = indexes['pages']
        self.__indexes_bm25 = []
        self.__k = k
        self.__b = b
        self.__epsilon = e
        self.__content_len = {}
        self.__avgdl = 0
        self.__token_idfs = {}
        self.__calculate_avg_doc_len()

    def __calculate_avg_doc_len(self):
        """
            Calcula la longitud media de los documentos y la longitud del contenido total.
        """
        # cada page_id es el identicador de cada pagina
        for page_id in self.__pages:
            title = self.__pages[page_id]['title']
            if not title:
                title = ""
            title = title.split(' ')
            content = self.__pages[page_id]['content']
            full_text_len = len(title) + len(content)
            self.__content_len[page_id] = full_text_len
        
        # sumamos la longitud de los contenidos de cada pagina
        self.__avgdl = sum(self.__content_len[page_id] for page_id in self.__content_len)
        # calculamos avgdl (Average documents length)
        self.__avgdl = self.__avgdl/len(self.__pages.keys())

    def term_frequency(self, token, page_id):
        """
        *Description:
            Se calcula la frecuncia de ocurrencia de un token/termino en una pagina con identificador 'page_id'.
            En bm25 tf(D,q) = [f(q,D)*(K+1)] / [f(t,D) + k*(1-b+b*D/avgl)]
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
        
        k = self.__k
        b = self.__b
        content_len = self.__content_len[page_id]
        # calculamos la frecuencia del token en la pagina __pages[page_id]
        numerator = freq * (k+1)
        denominator = freq + k * (1 - b + b * content_len / self.__avgdl)
        tf = numerator / denominator

        return tf

    def inverse_document_frequency(self):
        """
        *Description:
            Calcula la frecuencia de ocurrencia de todos los tokens en la colección de documentos/paginas,
            para medir que tan relevante es una palabra/token en una coleccion de documentos/paginas.
            En bm25 idf(q) = log( ((N-N(q)+0.5)/N(q)+0.5) + 1 )
        *Parameters
            @self
        *Returns
            @None
        """
        sum_idf = 0.0
        negative_idfs = []
        # el numero total de paginas
        N = len(self.__pages.keys())
        for token in self.__tokens:
            # el numero de documentos/paginas en el cual aparece el token (document frequency)
            df = len(self.__tokens[token])            
            # calculamos el idf del token correspondiente y lo guardamos
            idf = np.log(1 + (N - df + 0.5) / (df + 0.5))
            self.__token_idfs[token] = idf
            sum_idf += idf
            # guardamos los token con idf negativo
            if idf < 0:
                negative_idfs.append(token)
        # calculamos el average del total de tokens
        avg_idf = sum_idf / len(self.__token_idfs.keys())
        # actualizamos los idf para los tokens con idf negativos
        for token in negative_idfs:
            self.__token_idfs[token] = self.__epsilon * avg_idf

    def get_results (self):
        """
        *Description:
            Se obtiene el resultado actual de __indexes_bm25 con los datos de 
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
        for item in self.__indexes_bm25:
            page_id = item[0]
            # des_len = int(20 * len(self.__pages[page_id]['content'])/100)
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
            Ordena el contenido el resultado por relevancia, en orden decreciente.
        """
        # __indexes_tf_idf representa una lista de tuplas, list[(page_id1, score1), (page_id2, score2), ...]
        self.__indexes_bm25 = sorted(self.__indexes_bm25, key=lambda x: x[1], reverse=True)
    
    def rank_pages(self):
        """
        *Description:
            Puntua cada pagina obtenida del indexs para medir que tan relevante son
            cada paginas. Se aplica el metodo numerico BM25(q,D) = tf(q,D) * idf(q).
        *Parameters
            @self
        *Returns
            @None
        """
        # calculamos los idf de cada tokens
        self.inverse_document_frequency()
        # cada page_id es el identicador de cada pagina
        for page_id in self.__pages:
            score = 0.0
            for token in self.__tokens:
                # calculamos la frecuencia de ocurrencia del token en el contenido de la pagina con id page_id
                tf = self.term_frequency(token, page_id)
                # obtenemos la frecuencia de ocurrencia del token
                idf = self.__token_idfs[token]
                # aplicamos la formula de tf-idf = tf*idf para la puntuacion, y sumamos a cada puntuacion
                score += tf * idf
            self.__indexes_bm25.append((page_id, score))