from langdetect import detect, DetectorFactory, detect_langs
from langdetect.lang_detect_exception import LangDetectException
import datetime

DetectorFactory.seed = 0 # To enforce consistent results ( https://pypi.org/project/langdetect/ )

def language_detect(sentence: str)-> str:
    """Give a sentence 
    this function detect the language 

    e.g:
     language_detect('hola que tal')
     -> 'es'
    """
    ca = 0
    print(sentence)
    if 'ñ' in sentence:
        ca = 1

    # if the sentence is only numbers or is empty -> return unknown language
    if sentence.isdecimal() or not sentence:
        return 'unknown'
    language = detect(sentence)
    if language =='ca':
        language = 'es'
    return language


def language_detect_2(sentence: str) -> str:
    start_time = datetime.datetime.now()


    try:
        lang = detect(sentence)
        end_time = datetime.datetime.now()
        time_diff = (end_time - start_time)
        execution_time = time_diff.total_seconds() * 1000
        print("execution time in lang_detect_2", execution_time, "ms")
        if lang != "en":
            
            return "es"
    except LangDetectException: 
        # retorna un unknow cuando hay un error ya se le paso un url, numeros o no palabras
        # y por eso no detecto nada
        return "unknow"
    return "en"

    
    

if __name__ == '__main__':
    # return 'en' (english)
    print( language_detect_2("how to play the guitar"))
    print( language_detect_2("final examen schedule"))
    # return 'es' (spanish)
    print( language_detect_2("como tocar la guitarra"))
    print( language_detect_2("horarios de examenes finales"))
    print( language_detect_2("hilo"))
    print( language_detect_2("daklsdasjkd"))
    # return 'unknow'
    print( language_detect_2("https://www.comxdxd.com"))
    print( language_detect_2("123231"))
    print( language_detect_2("") )
