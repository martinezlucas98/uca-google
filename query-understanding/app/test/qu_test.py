import unittest

from app.nlp_tools.tokenizer import tokenizer
from app.nlp_tools.stopwords_filter import remove_stopwords
from app.nlp_tools.lemmatization import lemmatizer
from app.text_normalization import stemming

class QueryUnderstandingTest(unittest.TestCase):
    # def test_normalize_accents(self):
    #     self.assertEqual(normalize_accents('donde hay un balcón.'), 'donde hay un balcon.')
    #     self.assertEqual(normalize_accents('Enseñó'), 'Enseno')
        
        # Agregar para acentos nasales 

    def test_tokenizer_spacy(self):
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
    
    def test_lemmatization_spacy(self):
        self.assertEqual(
            first= lemmatizer(['hablando', 'jugando', 'jugar', 'comiendo', 'horarios', 'personas', 'ideas', 'cosas', 'yendo']),
            second= ['hablar', 'jugar', 'jugar', 'comer', 'horario', 'persona', 'idea', 'cosa','ir']
        )

    def test_stemming(self):
        self.assertEqual(
            first= stemming(['En', 'su', 'parte', 'de', 'arriba', 'encontramos', 'la', 'donde', 'se', 'puede', 'echar', 'el', 'detergente', 'aunque', 'en', 'nuestro', 'caso', 'lo', 'al', 'ser', 'gel', 'lo', 'ponemos', 'directamente', 'junto', 'con', 'la', 'ropa','.']),
            second= ['En', 'su', 'part', 'de', 'arrib', 'encontr', 'la',  'dond', 'se', 'pued', 'echar', 'el', 'detergent',  'aunqu', 'en', 'nuestr', 'cas', 'lo', 'al', 'ser', 'gel', 'lo', 'pon', 'direct', 'junt', 'con', 'la', 'rop', '.']

        )

    

        
        

if __name__ == '__main__':
    unittest.main()