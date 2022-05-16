from text_normalization import  normalize
from nlp_tools.named_entity import get_entity
from nlp_tools.part_of_speech import get_part_of_speech

def expand_query(sentence:str) -> dict : 
    response = {
        'original_sentence': sentence,
        'corrected_sentence': '',
        'language': '',
        'lemmatized_tokens': [],
        'stemmed_tokens': [],
        'query_expansion': {},
        'classification': '',
        'entity': {},
        'part_of_speech': {}
    }

    stemmed_tokens, lemmatized_tokens, corrected_sentence = normalize(sentence)
    entity = get_entity(corrected_sentence)
    part_of_speech = get_part_of_speech(corrected_sentence)

    
    response['corrected_sentence'] = corrected_sentence
    response['stemmed_tokens'] = stemmed_tokens
    response['lemmatized_tokens'] = lemmatized_tokens
    response['entity'] = entity
    response['part_of_speech'] = part_of_speech
    

    return response



if __name__ == '__main__':
    expand_query('!!#$%^tesiss  hablamos del 2019.')