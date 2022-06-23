from text_normalization import normalize
from nlp_tools.lang_detect import language_detect_2
import datetime


def only_lemma_stemm(sentence:str) -> dict : 
    """
    Do only lemmatization and Steaming to improve perfomance
    """
    response = {
        'status': 'ok',
        'original_sentence': sentence,
        'corrected_sentence': '',
        'language': '',
        'lemmatized_tokens': [],
        'stemmed_tokens': [],
        'query_expansion': [],
        'classification': ''
        #'entity': {},
        #'part_of_speech': {}
    }
    # first we need to detect the language, to pass the language as an argument in the others functions
    lang_detected = language_detect_2(sentence)  

    # if the sentence enter is not a something like url, only_digits or not detected language -> call function that use a language
    if lang_detected != 'unknow':
        clean, stemmed_tokens, lemmatized_tokens, corrected_sentence = normalize(sentence, lang=lang_detected)
    else:
        
        stemmed_tokens = []
        lemmatized_tokens = []
        corrected_sentence = []

    response['corrected_sentence'] = (' ').join(corrected_sentence)
    response['language'] = lang_detected #language
    response['stemmed_tokens'] = stemmed_tokens
    response['lemmatized_tokens'] = lemmatized_tokens

    return response