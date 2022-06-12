

import re
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
import datetime
import snowballstemmer



#from nlp_tools.spell_correction import spell_correction
from spellchecker import SpellChecker
from nlp_tools.stopwords_filter import remove_stopwords
from nlp_tools.lemmatization import lemmatizer

SPELL_CHECKER_SPANISH = SpellChecker(language='es')
SPELL_CHECKER_ENGLISH = SpellChecker() # The default is English

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

    start_time = datetime.datetime.now()
    

    result = re.sub(r'[^\w\s]','',input_text)

    end_time = datetime.datetime.now()
    time_diff = (end_time - start_time)
    execution_time = time_diff.total_seconds() * 1000
    print("execution time in cleaning",execution_time, "ms")
    
    return result

def tokenization(input_text):
    """Give a sentence
    return the statement 
    separated into tokens
    
    e.g:
     cleaning(['tesis del año 2019')
     -> ['tesis','del','año','2019']
    """
    start_time = datetime.datetime.now()

    word_token = nltk.word_tokenize(input_text)

    end_time = datetime.datetime.now()
    time_diff = (end_time - start_time)
    execution_time = time_diff.total_seconds() * 1000
    print("execution time in tokenization",execution_time, "ms")  
    return word_token

# Stemming del texto no estructurado, utilizando un diccionario de palabras
def stemming(input_text: list, lang='es') -> list:
    """Give a sentence
    returns the stemming of the sentence
    
    e.g:
     stemming('palabras y perros')
     -> ['palabr','y','perr']
    """
    start_time = datetime.datetime.now()
    if lang == 'en':    
        stemmer = snowballstemmer.stemmer('english')
    else:
        stemmer = snowballstemmer.stemmer('spanish')

    end_time = datetime.datetime.now()
    time_diff = (end_time - start_time)
    execution_time = time_diff.total_seconds() * 1000
    print("execution time in stemm",execution_time, "ms")    

    return stemmer.stemWords(input_text)

def normalize(input_text, lang='es'):

    start_time = datetime.datetime.now()


    if lang =='en':
        spell_checker_by_language = SPELL_CHECKER_ENGLISH # The default is English
    else:
        spell_checker_by_language = SPELL_CHECKER_SPANISH
        
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

    end_time = datetime.datetime.now()
    time_diff = (end_time - start_time)
    execution_time = time_diff.total_seconds() * 1000
    print("execution time in normalize",execution_time)
    
    return clean, stem, lem, spell_check_sentence

if __name__ == "__main__":
    print(normalize('!!#$%^tesiss del 2019.'))
