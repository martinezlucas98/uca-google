import unittest
import requests
import zlib
import json
import pickle

class IndexServerTest(unittest.TestCase):
    def test_search_full(self):
        res = requests.get('http://localhost:8080/full')
        self.assertGreater(len(res.json()), 0)
    
    def test_search_by_substrings(self):
        s = 'sub'
        res = requests.get(f'http://localhost:8080/subs?q={s}')
        self.assertEqual(len([word for word in res.json()['tokens'] if s not in word]), 0)
    
    def test_search_by_start(self):
        s = 'sub'
        res = requests.get(f'http://localhost:8080/st?q={s}')
        self.assertEqual(len([word for word in res.json()['tokens'] if not word.startswith(s)]), 0)
    
    def test_search_and_or(self):
        s = 'sub+test'
        rand = requests.get(f'http://localhost:8080/st?q={s}&f=and')
        ror = requests.get(f'http://localhost:8080/st?q={s}&f=or')
        self.assertGreaterEqual(len(ror.json()['pages']), len(rand.json()['pages']))
    
    def test_search_nolink(self):
        s = 'sub'
        res = requests.get(f'http://localhost:8080/st?q={s}&nolink=1')
        # get first page
        page = list(res.json()['pages'].keys())[0]
        self.assertRaises(KeyError, lambda: res.json()['pages'][page]['links'])
    
    def test_request_json(self):
        s = 'test'
        res = requests.get(f'http://localhost:8080/st?q={s}')
        self.assertEqual(len(res.json()), 2)
    
    def test_request_compressed(self):
        s = 'test'
        res = requests.get(f'http://localhost:8080/stc?q={s}')
        self.assertEqual(len(json.loads(zlib.decompress(res.content))), 2)
    
    def test_request_serialized(self):
        s = 'test'
        res = requests.get(f'http://localhost:8080/sts?q={s}')
        self.assertEqual(len(pickle.loads(res.content)), 2)
    
    def test_help(self):
        res = requests.get(f'http://localhost:8080/help')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-type'], 'text/html')

if __name__ == '__main__':
    # Requires running server @ localhost:8080
    unittest.main()