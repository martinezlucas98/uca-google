from googletrans import Translator
from langdetect import detect, DetectorFactory, detect_langs
from langdetect.lang_detect_exception import LangDetectException
import nltk
import re
DetectorFactory.seed = 0 # To enforce consistent results ( https://pypi.org/project/langdetect/ )

"""In this script we use several methods to be able to detect the language of a given statement. 
    Some libraries are non-deterministic, they are not very exact, but combining with
    other libraries, we get better results.
"""

def detect_lang_googletrans(sentence: str) -> str:
    """Given a sentence
        the detected language is returned
        using the googletrans lib
    e.g:
     detect_lang_googletrans(['tesis del año 2019')
     -> 'es'
    """
    translator = Translator()                               #First, initialize the class translator
    
    lang = translator.detect(sentence)                      #Detect the language of the statement
    print("aqui hay un bug")
    if lang.lang == 'es' :                                     
        result ='es'                                        #Store the resulting language. If is english store 'en' or if is Spanish 'es'
    elif lang.lang == 'en':                                         
        result = 'en'                                       #If the language detected if another, we store as 'other'
    else:                                                   
        result = 'other'
    
    return result

def detect_lang_langdetect(sentence: str) -> str:
    """Given a sentence
        the detected language is returned
        using the lang detect lib

    e.g:
     detect_lang_langdetect(['tesis del año 2019')
     -> 'es'
    """
    lang = []
    try:
        lang = detect_langs(sentence)                           #Call the function to detect the language of the sentence
        lang = str(lang)                                        #Convert to a string
    except LangDetectException:
        return 'unknow'                                         #If an error occurs, return the language detected as unknow
    if 'es' in lang:                                            #If the language is spanish, it returns 'es'
        result = 'es'
    elif 'en' in lang:                                          #If the language is english, it returns 'en'
        result = 'en'
    else:
        result = 'other'                                        #If the language is another, it returns 'other'
    return result

def detect_lang_swnltk(sentence: str) -> str:
    """Given a sentence
        the detected language is returned
        using the nltk lib

    e.g:
     detect_lang_swnltk('tesis del año 2019')
     -> 'es'
    """
    languages = ["spanish","english"]                                       #Only detected two languages: english or spanish
    tokens = nltk.tokenize.word_tokenize(sentence)                          #Tokenize the sentence
    tokens = [t.strip().lower() for t in tokens]                            #Convert all texts to lowercase for later comparison
    lang_count = {}                                                         #Initialize a dict where we will store the count of stopwords for each language
    for lang in languages:
        stop_words = set(nltk.corpus.stopwords.words(lang))
        lang_count[lang] = 0                                                #Initialize the counter for each language
        for word in tokens:
            if word in stop_words:                                          #If the word is in the stopwords, increment the counter for the language
                lang_count[lang] += 1
    result = max(lang_count, key=lang_count.get)                            #Stores the language that had the highest counter
    if result == 'spanish':
        result = 'es'
    else:
        result = 'en'
    return result

def language_detect2(sentence: str) -> str:
    """Given a sentence
        the detected language is returned
        using the above functions 

    e.g:
     language_detect2('tesis del año 2019')
     -> 'es'
    """
    sentence = ''.join([i for i in sentence if not i.isdigit()])                        #Remove the numeric values ​​if they exist
    sentence = re.sub(r'[^\w\s]','',sentence)                                           #Remove non-letter characters
    result_detectlang = detect_lang_langdetect(sentence)                                #First, call the function langdetect
    try:
        
        result_lang_google = detect_lang_googletrans(sentence)                          #Call the function googletrans
        result_lang_stopw = detect_lang_swnltk(sentence)                                #Call the funcition stopwords nltk
        if result_lang_google == result_lang_stopw:                                     #If the results are equal, then store that language
            return result_lang_google
        else:                                                                           #If not, store 'es' like the default language or unknow if is not recognize
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
