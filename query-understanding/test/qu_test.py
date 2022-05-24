import unittest

from nlp_tools.tokenizer import tokenizer
from text_normalization import tokenization
from nlp_tools.lang_detect import language_detect
from nlp_tools.stopwords_filter import remove_stopwords
from nlp_tools.lemmatization import lemmatizer
from text_normalization import stemming, tokenization, cleaning
from nlp_tools.query_expansion import entity_recongnition, query_expansion
import main as endpoints


class QueryUnderstandingTest(unittest.TestCase):
    # def test_normalize_accents(self):
    #     self.assertEqual(normalize_accents('donde hay un balcón.'), 'donde hay un balcon.')
    #     self.assertEqual(normalize_accents('Enseñó'), 'Enseno')
        
        # Agregar para acentos nasales 
    def test_tokenization_spacy(self):
        self.assertEqual(
            tokenizer(''),
            []
        )
        self.assertEqual(
            tokenizer('123'),
            ['123']
        )
        self.assertEqual(
            tokenizer('!dsd !'),
            ['!', 'dsd', '!']
        )
        self.assertEqual(
            tokenizer('Horarios de clases de economía.'),
            ['Horarios', 'de', 'clases', 'de', 'economía', '.' ]
        )
        self.assertEqual(
            tokenizer('Hola!'),
            [ 'Hola', '!']
        )
        self.assertEqual(
            tokenizer("me alegro, que tal todo?"),
            ['me', 'alegro', ',', 'que', 'tal', 'todo', '?' ]
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

         
    def test_stemming(self):
        self.assertEqual(
            first= stemming([]),
            second=[]
        )
        self.assertEqual(
            first= stemming(['12', '']),
            second=['12', '']
        )
        self.assertEqual(
            first= stemming(['En', 'su', 'parte', 'de', 'arriba', 'encontramos', 'la', 'donde', 'se', 'puede', 'echar', 'el', 'detergente', 'aunque', 'en', 'nuestro', 'caso', 'lo', 'al', 'ser', 'gel', 'lo', 'ponemos', 'directamente', 'junto', 'con', 'la', 'ropa','.']),
            second= ['En', 'su', 'part', 'de', 'arrib', 'encontr', 'la',  'dond', 'se', 'pued', 'echar', 'el', 'detergent',  'aunqu', 'en', 'nuestr', 'cas', 'lo', 'al', 'ser', 'gel', 'lo', 'pon', 'direct', 'junt', 'con', 'la', 'rop', '.']
        )
        
        
    def test_remove_stopwords(self):
        self.assertEqual(
            first= remove_stopwords(['','12', '0']),
            second= ['','12', '0']
        )
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
            first= lemmatizer(['12','','hablando', 'jugando', 'jugar', 'comiendo', 'horarios', 'personas', 'ideas', 'cosas', 'yendo']),
            second= ['12',' ','hablar', 'jugar', 'jugar', 'comer', 'horario', 'persona', 'idea', 'cosa','ir']
        )

    
    def test_cleaning(self):
        self.assertEqual(
            first=cleaning(''),
            second= ''
        )
        self.assertEqual(
            first=cleaning('123456789'),
            second='123456789'
        )
        self.assertEqual(
            first=cleaning('!!! hola, a todos; que tal amigos.;;;?? ? / ??'),
            second=' hola a todos que tal amigos   '
        )
        self.assertEqual(
            first=cleaning('!!1 23456789??../'),
            second='1 23456789'
        )
        self.assertEqual(
            first=cleaning('!!??../'),
            second=''
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
        self.assertEqual(
            first=type(entity_recongnition('')),
            second=str
        ),
        self.assertEqual(
            first=type(entity_recongnition('1234')),
            second=str
        ),
        self.assertEqual(
            first=type(entity_recongnition('hol aque tal !')),
            second=str
        ),
        self.assertEqual(
            first=type(entity_recongnition('!??!')),
            second=str
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

        
    def test_endpoint_expand_query(self):
        response = endpoints.expand_query_route(q='')
        self.assertEqual(
            first= response['status'],
            second= 'empty query'
        )
        response = endpoints.expand_query_route(q='añoss')
        self.assertEqual(response['status'],second= 'ok')
        self.assertEqual(response['original_sentence'], 'añoss')
        self.assertEqual(response['corrected_sentence'], 'años')
        self.assertEqual(response['lemmatized_tokens'], ["año"])
        self.assertEqual(response['stemmed_tokens'], ["años"])
        self.assertEqual(response['query_expansion'],
            [
                "ańos",
                "meses",
                "lustros",
                "décadas",
                "edad",
                "ochenta",
                "noventa",
                "anos",
                "sesenta",
                "setenta"
            ]
        )
    
    
if __name__ == '__main__':
    unittest.main()
