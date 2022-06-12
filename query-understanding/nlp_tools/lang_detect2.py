from googletrans import Translator
from langdetect import detect, DetectorFactory, detect_langs
from langdetect.lang_detect_exception import LangDetectException
import nltk
DetectorFactory.seed = 0 # To enforce consistent results ( https://pypi.org/project/langdetect/ )


def detect_lang_googletrans(sentence: str) -> str:
    translator = Translator()
    lang = translator.detect(sentence)
    if lang.lang == 'es' : 
        result ='es'
    elif lang.lang == 'en':
        result = 'en'
    else:
        result = 'other'
    return result

def detect_lang_langdetect(sentence: str) -> str:
    lang = []
    try:
        lang = detect_langs(sentence)
        lang = str(lang)
    except LangDetectException:
        return 'unknow'
    if 'es' in lang: 
        result = 'es'
    elif 'en' in lang:
        result = 'en'
    else:
        result = 'other'
    return result

def detect_lang_swnltk(sentence: str) -> str:
    languages = ["spanish","english"]
    tokens = nltk.tokenize.word_tokenize(sentence)
    tokens = [t.strip().lower() for t in tokens] # Convierte todos los textos a minúsculas para su posterior comparación
    # Creamos un dict donde almacenaremos la cuenta de las stopwords para cada idioma
    lang_count = {}
    for lang in languages:
        stop_words = set(nltk.corpus.stopwords.words(lang))
        lang_count[lang] = 0 # Inicializa a 0 el contador para cada idioma
        # Recorremos las palabras del texto a analizar
        for word in tokens:
            #print(stop_words)
            if word in stop_words: # Si la palabra se encuentra entre las stopwords, incrementa el contador
                lang_count[lang] += 1
        # Recorremos las palabras del texto a analizar
    result = max(lang_count, key=lang_count.get) 
    if result == 'spanish':
        result = 'es'
    else:
        result = 'en'
    return result

def language_detect2(sentence: str) -> str:
    sentence = ''.join([i for i in sentence if not i.isdigit()])
    result_detectlang = detect_lang_langdetect(sentence)
    try:
        result_lang_google = detect_lang_googletrans(sentence)
        result_lang_stopw = detect_lang_swnltk(sentence)
        if result_lang_google == result_lang_stopw:
            return result_lang_google
        else:
            if result_lang_google != 'other': 
                return 'es'
            else:
                if result_detectlang == 'en' or result_detectlang == 'es':
                   return result_detectlang
                return 'unknow'
    except: 
        return 'unknow'


if __name__ == '__main__':
    #return 'en' (english)
    print( language_detect2("how to play the guitar"))
    print('\n')
    print( language_detect2("examen final schedule"))
    print('\n')
    #return 'es' (spanish)
    print( language_detect2("como tocar la guitarra"))
    print('\n')
    print( language_detect2("horarios de examenes finales"))
    print('\n')
    print( language_detect2("hilo"))
    print('\n')
    # #return 'unknow'
    print( language_detect2("https://www.comxdxd.com"))
    print('\n')
    print( language_detect2("hola123231"))
    print('\n')
    print( language_detect2("") )
    print(language_detect2("daklsdasjkd"))
    print('\n')
