import re
import nltk
#nltk.download('punkt')
#nltk.download('wordnet')
#nltk.download('omw-1.4')
import hunspell
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Preprocesamiento de datos
'''
    Seguimos los siguientes pasos:
        1. Limpieza del texto
        2. Tokenization
        3. Stemming & Lemmatization
'''


# Limpieza del texto no estructurado
def cleaning(input_text):
    return re.sub(r'[^\w\s]','',input_text)

# Tokenization del texto no estructurado
def tokenization(input_text):
    word_token = nltk.word_tokenize(input_text)
    return word_token

# Stemming del texto no estructurado, utilizando un diccionario de palabras
def stemming(input_text):
    dic = hunspell.HunSpell("es_ANY.dic", "es_ANY.aff")
    stemmer = PorterStemmer()
    #input_text = nltk.word_tokenize(input_text)
    words_stemm = []
    for word in input_text:
        w_stem = stemmer.stem(word)
        if dic.spell(w_stem):               # Si la palabra con stemming se encuentra en el dic
            words_stemm.append(w_stem)
        else:
            words_stemm.append(word)        # Si no se encuentra, se agrega la palabra sin stemm
    return words_stemm

def lemmatization(input_text):
    lemmatizer = WordNetLemmatizer()
    #input_text = nltk.word_tokenize(input_text)
    words = []
    for word in input_text:
        word_lem = lemmatizer.lemmatize(word)
        words.append(word_lem)
    return words

def normalize(input_text):
    #limpiamos
    clean = cleaning(input_text)
    #tokenizamos
    tokenize = tokenization(clean)
    #stemming
    stem = stemming(tokenize)
    #lemmatization
    lem = lemmatization(tokenize)
    return stem,lem
print(normalize('!!#$%^tesis del 2019'))