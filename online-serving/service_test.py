
import unittest
import requests
import json

from search_modules.pageRank import pagerank, generate_pages
from settings import PATH_INDEX, PATH_QUERY, PATH_ONLINE
from search import search


class ServiceTest(unittest.TestCase):
    def test_index_service(self):
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

    @unittest.expectedFailure
    def test_rank_pageRank(self):
        # si se actualiza el indice con el crawler estos datos de prueba puede ser que 
        # estos datos ya no sean validos.
        data = [
            'http://www.universidadcatolica.edu.py/preguntas-frecuentes/',
            'https://www.universidadcatolica.edu.py/admision-2/', 
            'https://www.universidadcatolica.edu.py/author/uc/'
        ]
        pages = search("curso de testing?")
        pages = json.loads(pages)
        pages  = pages['results']
        pages = [page['url'] for page in pages]
        self.assertEqual(
            first = pages, 
            second = data
        )
    
    def test_prob_pageRank(self):
        pages = requests.get(PATH_INDEX + "st?q=curso+de+testing").json()
        pages = generate_pages(pages)
        ranked_pages = pagerank(pages)
        count = 0.0
        for page in ranked_pages.keys():
            count += ranked_pages[page]
        count = round(count)
        self.assertEqual(
            first = count == 1.0, 
            second = True
        )

    def test_page_not_found(self):
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
    def test_search(self):
        r = requests.get(PATH_ONLINE + "search?q=curso+de+testing").json()
        r = json.loads(r)
        self.assertEqual(
            first = r['status'] == "success", 
            second= True
        )

    def test_empty_search(self):
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

   

    