import string
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

def tokenize_query(query: str):
    """
        Retorna el query tokenizado.
        Ej:
        query = "¿Donde queda ubicado Paraguay?"
        return ['queda', 'ubicado', 'paraguay']
    """
    STOP_WORDS = stopwords.words('spanish')
    query_tokens = word_tokenize(query)
    query_tokens = [tk.lower() for tk in query_tokens]

    # eliminar los signos de puntuacion (?,?,!,(),#,etc) de cada token
    re_punc = re.compile('[%s]' % re.escape(string.punctuation))
    query_tokens = [re_punc.sub('', tk) for tk in query_tokens]
    query_tokens = [tk for tk in query_tokens if tk.isalpha()]

    #eliminar los stop words
    query_tokens = [tk for tk in query_tokens if tk not in STOP_WORDS]
    
    return query_tokens
    