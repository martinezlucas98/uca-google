import unittest
from text_normalization import normalize_accents
from nlp_tools.tokenization.tokenizer import tokenizer


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
        

if __name__ == '__main__':
    unittest.main()