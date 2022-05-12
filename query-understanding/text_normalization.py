import unidecode
from nlp_tools.spell_correction import spell_correction
from nlp_tools.tokenizer import tokenizer
from nlp_tools.lemmatization import lemmatizer
from nlp_tools.stopwords_filter import remove_stopwords

def text_normalization(sentence: str): 

    # put here a function to remove . , ? ! ect...
    tokenized = tokenizer(sentence=sentence)
    lemmatized = lemmatizer(tokenized)
    stopwords_removed = remove_stopwords(lemmatized) 

    # words_corrected = [spell_correction.correction(word) for word in sentence.split()]
    # corrected_sentence = ' '.join(words_corrected)

    # corrected_sentence = normalize_accents(corrected_sentence)

    

    return ''
    

    



def normalize_accents(sentece: str) -> str:
    """Change whatever word with an accent to the ASCII version of the letter
    e.g: 
        'áÁ' ->'aA'
             
    """
    return unidecode.unidecode(sentece)


if __name__ == "__main__":
    print(text_normalization("hola que . , tall vámoss al cune hoy?"))