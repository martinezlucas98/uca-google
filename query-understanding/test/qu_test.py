import unittest
from text_normalization import normalize_accents
from nlp_tools.tokenizer import tokenizer
from nlp_tools.stopwords_filter import remove_stopwords

class QueryUnderstandingTest(unittest.TestCase):
    def test_normalize_accents(self):
        self.assertEqual(normalize_accents('donde hay un balcón.'), 'donde hay un balcon.')
        self.assertEqual(normalize_accents('Enseñó'), 'Enseno')
        
        # Agregar para acentos nasales 

    def test_tokenizer(self):
        self.assertEqual(
            tokenizer('Horarios de clases de economía.'),
            ['Horarios', 'de', 'clases', 'de', 'economía', '.' ]
        )
        self.assertEqual(
            tokenizer('¡Hola!'),
            ['¡', 'Hola', '!']
        )

        self.assertEqual(
            tokenizer("me alegro, que tal todo?"),
            ['me', 'alegro', ',', 'que', 'tal', 'todo', '?' ]
        )

    def test_remove_stopwords(self):
        self.assertEqual(
            first= remove_stopwords(['Copa', 'Mundial', 'de', 'Fútbol']),
            second= ['Copa', 'Mundial', 'Fútbol']
            
        )
        self.assertEqual(
            first= remove_stopwords(['Día', 'de', 'la', 'Enfermera']),
            second= ['Día', 'Enfermera']
            
        )
        self.assertEqual(
            first= remove_stopwords(['Ayer', 'vi', 'a', 'tu', 'hermano', 'por', 'la', 'calle']),
            second= ['Ayer', 'vi', 'hermano',  'calle']
            
        )
        
        

if __name__ == '__main__':
    unittest.main()