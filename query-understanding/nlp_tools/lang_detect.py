from langdetect import detect


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

    language = detect(sentence)
    if language =='ca' and ca:
        language = 'es'
    return language

if __name__ == '__main__':
    print(language_detect('tesis del año.. '))
