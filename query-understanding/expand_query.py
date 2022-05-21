from text_normalization import  normalize
from nlp_tools.named_entity import get_entity
from nlp_tools.part_of_speech import get_part_of_speech
from nlp_tools.query_expansion.query_expansion import query_expansion, entity_recongnition

def expand_query(sentence:str) -> dict : 
    response = {
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

    clean,stemmed_tokens, lemmatized_tokens, corrected_sentence = normalize(sentence)
    #entity = get_entity(corrected_sentence)
    classification = entity_recongnition(clean)
    query_expan = query_expansion(corrected_sentence)
    #part_of_speech = get_part_of_speech(corrected_sentence)

    
    response['corrected_sentence'] = corrected_sentence
    response['stemmed_tokens'] = stemmed_tokens
    response['lemmatized_tokens'] = lemmatized_tokens
    #response['entity'] = entity
    #response['part_of_speech'] = part_of_speech
    response['classification'] = classification
    response['query_expansion'] = query_expan

    return response



if __name__ == '__main__':
    final_query = expand_query('!!#$%^tesis del 2019.')
    for value,key in final_query.items():
        print(value,': ',key)