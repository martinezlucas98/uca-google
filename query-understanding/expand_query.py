from text_normalization import  normalize

from nlp_tools.lang_detect import language_detect, language_detect_2
from nlp_tools.lang_detect2 import language_detect2
from nlp_tools.query_expansion import query_expansion, entity_recongnition

def expand_query(sentence:str) -> dict : 
    response = {
        'status': 'ok',
        'original_sentence': sentence,
        'corrected_sentence': '',
        'language': '',
        'lemmatized_tokens': [],
        'stemmed_tokens': [],
        'query_expansion': [],
        #'classification': ''
        #'part_of_speech': {}
    }
    # first we need to detect the language, to pass the language as an argument in the others functions
    lang_detected = language_detect2(sentence)  


    

    # if the sentence enter is not a something like url, only_digits or not detected language -> call function that use a language
    if lang_detected != 'unknow':
        clean, stemmed_tokens, lemmatized_tokens, corrected_sentence = normalize(sentence, lang=lang_detected)
        query_expan = query_expansion(corrected_sentence)
       
    else:
        clean =''
        stemmed_tokens = []
        lemmatized_tokens = []
        corrected_sentence = []
        query_expan = []

    
    response['corrected_sentence'] = (' ').join(corrected_sentence)
    response['language'] = lang_detected #language
    response['stemmed_tokens'] = stemmed_tokens
    response['lemmatized_tokens'] = lemmatized_tokens
    response['query_expansion'] = query_expan
    #response['classification'] = classification
    #response['part_of_speech'] = part_of_speech
    return response


if __name__ == '__main__':
    final_query = expand_query('!!#$%')
    for value,key in final_query.items():
        print(value,': ',key)
