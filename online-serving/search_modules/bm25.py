import math

class BM25():
    def __init__(self, indexes, k=1.2, b=0.75):
        self.__tokens = indexes['tokens']
        self.__pages = indexes['pages']
        self.__indexes_bm25 = []
        self.__k = k
        self.__b = b
        self.__content_len = {}
        self.__avgdl = 0
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

    def inverse_document_frequency(self, token):
        """
        *Description:
            Calcula la frecuencia de ocurrencia del token en la colección de documentos/paginas,
            para medir que tan relevante es una palabra/token en una coleccion de documentos/paginas.
            En bm25 idf(q) = log( ((N-N(q)+0.5)/N(q)+0.5) + 1 )
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
        return math.log(1 + (N - df + 0.5) / (df + 0.5))


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
            results.append(
                {
                    "url": self.__pages[page_id]['url'],
                    "title": self.__pages[page_id]['title'],
                    "description": self.__pages[page_id]['description']
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
        # cada page_id es el identicador de cada pagina
        for page_id in self.__pages:
            score = 0.0
            for token in self.__tokens:
                # calculamos la frecuencia de ocurrencia del token en el contenido de la pagina con id page_id
                tf = self.term_frequency(token, page_id)
                # calculamos la frecuencia de ocurrencia del token en todas las paginas
                idf = self.inverse_document_frequency(token)
                # aplicamos la formula de tf-idf = tf*idf para la puntuacion, y sumamos a cada puntuacion
                score += tf * idf
            self.__indexes_bm25.append((page_id, score))
