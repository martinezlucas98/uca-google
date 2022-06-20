
import unittest
import requests
import json

from search_modules.pageRank import GraphPageRank
from search_modules.tf_idf import TfIdf
from search_modules.bm25 import BM25
from settings import PATH_INDEX, PATH_QUERY, PATH_ONLINE
from search import search


class ServiceTest(unittest.TestCase):
    """
    Testea la conexion con los servicios externos.
    """

    def test_index_service(self):
        """
        Test de la conexion con el servicio Index.
        """
        flg = True
        try:
            response = requests.get(PATH_INDEX)
            response.raise_for_status()
        except Exception as err:
            flg = False
        else:
            pass
        self.assertEqual(
            first = flg, 
            second = True
        )

    def test_query_service(self):
        """
        Test de la conexion con el servicio query-understanding.
        """
        flg = True
        try:
            response = requests.get(PATH_QUERY)
            response.raise_for_status()
        except Exception as err:
            flg = False
        else:
            pass
        self.assertEqual(
            first = flg, 
            second = True
        )

class SearchTest(unittest.TestCase):
    """
    Testea los diferentes casos de busquedas, con los diferentes algoritmos
    de ranking.
    """

    def test_pageRank(self):
        """
        Test de la puntuacion del algoritmo pageRank sea correcto        
        """
        indexes = requests.get(PATH_INDEX + "st?q=pasantia+uca").json()
        # se instancia y se puntua.
        page_rank = GraphPageRank()
        page_rank.init(indexes['pages'])
        page_rank.pagerank()
        pages = page_rank.nodes
        # se debe cumplir que la suma de todas puntuacion sea igual a uno.
        count = 0.0
        for page in pages:
            count += pages[page]['score']
        count = round(count)
        #verificamos
        self.assertEqual(
            first = count == 1.0, 
            second = True
       )

    def test_bm25_tf_idf(self):
        """
        Test term frequency (tf) de bm25 y tf-idf siempre deben ser distintos
        """
        indexes = requests.get(PATH_INDEX + "st?q=informatica").json()
        # obtenemos e primer token
        token = list(indexes['tokens'].keys())
        token = token[0]
        # obtenemos la primera pagina relacionada del token
        page_id = indexes['tokens'][token]
        page_id = list(page_id.keys())
        page_id = page_id[0]
        # instanciamos bm25 y obtenemos el tf para token en el contenido de page_id
        bm25 = BM25(indexes)
        bm25_tf = bm25.term_frequency(token, page_id)
        # instanciamos tf-idf y obtenemos el tf para token en el contenido de page_id
        tfidf = TfIdf(indexes)
        tfidf_tf = tfidf.term_frequency(token, page_id)
        # si el token se encuentra en la pagina con page_id, ambas tf deben ser diferentes
        check = bm25_tf != tfidf
        # ambas tf coinciden cuando el token no se encuentra en la pag.
        if (bm25_tf == 0 and tfidf == 0):
            check = True

        self.assertEqual(
            first = check, 
            second = True
        )

    def test_page_not_found(self):
        """
        Test de ciertas palabras en otro idioma (en guarani) no obtenga resultado
        """
        results = search("mbarakaja")
        results = json.loads(results)

        results2 = search("karai")
        results2 = json.loads(results2)
        self.assertEqual(
            first = results['status'] == "notfound", 
            second = True
        )
        self.assertEqual(
            first = results2['status'] == "notfound", 
            second = True
        )

    def test_stop_words(self):
        """
        Test de busqueda de palabras que solo contienen stopwords
        """
        results = search("que")
        results = json.loads(results)

        results2 = search("que hay")
        results2 = json.loads(results2)
        self.assertEqual(
            first = results != None, 
            second = True
        )
        self.assertEqual(
            first = results2 != None, 
            second = True
        )

class OnlineServingTest(unittest.TestCase):
    """
    Testea que el servicio online-serving funcione correctamente.
    """

    def test_search(self):
        """
        Test online-serving busqueda valida
        """
        r = requests.get(PATH_ONLINE + "search?q=curso+de+test").json()
        r = json.loads(r)
        self.assertEqual(
            first = r['status'] == "success", 
            second= True
        )

    def test_empty_search(self):
        """
        Test online-serving para busquedas vacias
        """
        r = requests.get(PATH_ONLINE + "search?q=").json()
        r = json.loads(r)
        self.assertEqual(
            first = r['status'] == "notfound", 
            second= True
        )


if __name__ == "__main__":
    # print('test_pruebas')
    print(">>> SERVICES REQUEST TESTS:")
    suite = unittest.TestLoader().loadTestsFromTestCase(ServiceTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

    print("\n>>> SEARCH TESTS:")
    suite = unittest.TestLoader().loadTestsFromTestCase(SearchTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

    print("\n>>> REQUEST SERVICES:")
    suite = unittest.TestLoader().loadTestsFromTestCase(OnlineServingTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
 