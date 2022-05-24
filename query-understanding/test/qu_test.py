import unittest

from nlp_tools.tokenizer import tokenizer
from text_normalization import tokenization
from nlp_tools.lang_detect import language_detect
from nlp_tools.query_expansion import query_expansion, entity_recongnition
from nlp_tools.stopwords_filter import remove_stopwords
from nlp_tools.lemmatization import lemmatizer
from text_normalization import stemming

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

    def test_tokenizer(self):
        self.assertEqual(
            tokenization('Horarios de clases de economía'),
            ['Horarios', 'de', 'clases', 'de', 'economía']
        )
        self.assertEqual(
            tokenization('Hola como andan'),
            ['Hola', 'como', 'andan']
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
    
    def test_query_expansion(self):
        self.assertEqual(
            first= query_expansion(['días','feriados']),            
            second= ["meses","semanas","dias","mes","semana","laborables","transcurridos","años","horas","transcurridas"]
        )
        self.assertEqual(
            first= query_expansion(['reina','de','inglaterra']),
            second= ['princesa','reinas','rey','isabel','infanta','consorte','monarca','coronación','infantas','regente']
        )

    def test_entity_recongnition(self):
        self.assertEqual(
            first = entity_recongnition('carrera de informatica'),
            second = 'carrera'
        )
        self.assertEqual(
            first = entity_recongnition('un cuarto de carne'),
            second = 'carne'
        )
    def test_language_detect(self):
        self.assertEqual(
            language_detect('carrera de informatica'),
            'es'
        )
        self.assertEqual(
            language_detect('this is a test'),
            'en'
        )

        
if __name__ == '__main__':
    unittest.main()
