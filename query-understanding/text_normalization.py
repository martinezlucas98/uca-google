

import re
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

import snowballstemmer


#from nlp_tools.spell_correction import spell_correction
from spellchecker import SpellChecker
from nlp_tools.stopwords_filter import remove_stopwords
from nlp_tools.lemmatization import lemmatizer

# Preprocesamiento de datos
'''
    Seguimos los siguientes pasos:
        1. Limpieza del texto
        2. Tokenization
        3. Stemming & Lemmatization
'''
 


def cleaning(input_text):
    """Give a sentence
    remove characters 
    and returns a clean sentence

    e.g:
     cleaning(['!!#$%^tesis del año 2019.')
     -> 'tesis del año 2019'
    """
    return re.sub(r'[^\w\s]','',input_text)

def tokenization(input_text):
    """Give a sentence
    return the statement 
    separated into tokens
    
    e.g:
     cleaning(['tesis del año 2019')
     -> ['tesis','del','año','2019']
    """
    word_token = nltk.word_tokenize(input_text)
    return word_token

# Stemming del texto no estructurado, utilizando un diccionario de palabras
def stemming(input_text: list, lang='es') -> list:
    """Give a sentence
    returns the stemming of the sentence
    
    e.g:
     stemming('palabras y perros')
     -> ['palabr','y','perr']
    """

    if lang == 'en':    
        stemmer = snowballstemmer.stemmer('english')
    else:
        stemmer = snowballstemmer.stemmer('spanish')

    return stemmer.stemWords(input_text)

def normalize(input_text, lang='es'):

    if lang =='en':
        spell_checker_by_language = SpellChecker() # The default is English
    else:
        spell_checker_by_language = SpellChecker(language='es')
        
    #Cleaning
    clean = cleaning(input_text)
    #Tokenize
    tokenize = tokenization(clean)
    #Correct typos
    spell_check_sentence = [spell_checker_by_language.correction(token) for token in tokenize]
    #Remove stopwords( 'de', 'la', 'del')
    tokenize = remove_stopwords(spell_check_sentence)
    #Stemming
    stem = stemming(tokenize, lang)
    #Lemmatization
    lem = lemmatizer(tokenize, lang)
    
    return clean, stem, lem, spell_check_sentence

if __name__ == "__main__":
    print(normalize('!!#$%^tesiss del 2019.'))
