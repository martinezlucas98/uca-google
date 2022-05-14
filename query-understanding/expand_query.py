from text_normalization import  normalize

def expand_query(sentence:str) -> dict : 
    response = {
        'language': '',
        'lemmatized_tokens': [],
        'stemmed_tokens': [],
        'query_expansion': {

        },
        'classification': ''
    }

    stemmed_tokens, lemmatized_tokens = normalize(sentence)
    print(stemmed_tokens, lemmatized_tokens)

    response['stemmed_tokens'] = stemmed_tokens
    response['lemmatized_tokens'] = lemmatized_tokens

    return response



if __name__ == '__main__':
    expand_query('!!#$%^tesiss  hablamos del 2019.')