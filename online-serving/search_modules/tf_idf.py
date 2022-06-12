import math

class TfIdf:
    def __init__(self, indexes):
        self.__tokens = indexes['tokens']
        self.__pages = indexes['pages']
        self.__indexes_tf_idf = []
             
    def get_tf_idf_rank(self):
        return self.__indexes_tf_idf

    def term_frequency(self, token, page_id):
        """
            La frecuncia de ocurrencia de un token 'token' en una pagina 'page_id'.
        """
        count = 0
        try:
            count = self.__tokens[token][page_id]
        except Exception as err:
            pass
        
        title = self.__pages[page_id]['title']
        if not title:
            title = ""    

        # full_text = self.__pages[page_id]['title'] + self.__pages[page_id]['content']
        full_text = title + self.__pages[page_id]['content']
        return count / len(full_text)

    def inverse_document_frequency(self, token):
        df = len(self.__tokens[token])
        return math.log10(len(self.__pages) / (df + 1))


    def get_results (self):
        results = []
        for item in self.__indexes_tf_idf:
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
        self.__indexes_tf_idf = sorted(self.__indexes_tf_idf, key=lambda page: page[1], reverse=True)

    def rank_pages(self):
        # tokens_id = self._get_tokens_id()
        # corpus = [self.__pages[str(id)] for id in set.union(*tokens_id)]

        # puntuamos cada pagina del corpus
        # @todo: solo puntua mas el body, ver como mejorar tambien con el titulo
        results = []
        for page_id in self.__pages:
            score = 0.0
            for token in self.__tokens:
                tf = self.term_frequency(token, page_id)
                idf = self.inverse_document_frequency(token)
                score += tf * idf
            self.__indexes_tf_idf.append((page_id, score)) 