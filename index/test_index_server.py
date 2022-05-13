import unittest
import requests

class IndexServerTest(unittest.TestCase):
    def test_search_full(self):
        res = requests.get('http://localhost:8080/full')
        self.assertGreater(len(res.json()), 0)
    
    def test_search_by_initials(self):
        i = 'p'
        res = requests.get(f'http://localhost:8080/i?q={i}')
        self.assertEqual(len([word for word in res.json() if word[0] != i]), 0)
    
    def test_search_by_substrings(self):
        s = 'sub'
        res = requests.get(f'http://localhost:8080/subs?q={s}')
        self.assertEqual(len([word for word in res.json() if s not in word]), 0)
    
    def test_search_by_start(self):
        s = 'sub'
        res = requests.get(f'http://localhost:8080/st?q={s}')
        self.assertEqual(len([word for word in res.json() if not word.startswith(s)]), 0)
    
    def test_help(self):
        res = requests.get(f'http://localhost:8080/help')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-type'], 'text/html')

if __name__ == '__main__':
    # Requires running server @ localhost:8080
    unittest.main()