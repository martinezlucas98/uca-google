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

    # if the sentence is only numbers or is empty -> return unknown language
    if sentence.isdecimal() or not sentence:
        return 'unknown'
    language = detect(sentence)
    if language =='ca' and ca:
        language = 'es'
    return language

if __name__ == '__main__':
    print(language_detect('tesis del año.. '))
    print(language_detect('112s'))
