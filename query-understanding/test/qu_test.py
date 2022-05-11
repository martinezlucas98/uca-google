import unittest
from text_normalization import normalize_accents



class QueryUnderstandingTest(unittest.TestCase):
    def test_normalize_accents(self):
        self.assertEqual(normalize_accents('donde hay un balcón.'), 'donde hay un balcon.')
        self.assertEqual(normalize_accents('Enseñó'), 'Enseno')
        
        # Agregar para acentos nasales 
        

if __name__ == '__main__':
    unittest.main()