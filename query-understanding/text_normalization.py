import unidecode
from nlp_tools.spell_correction import spell_correction
from nlp_tools.tokenization import tokenizer

def text_normalization(sentence: str):

    # put here a function to remove . , ? ! ect...
    
    words_corrected = [spell_correction.correction(word) for word in sentence.split()]
    corrected_sentence = ' '.join(words_corrected)

    corrected_sentence = normalize_accents(corrected_sentence)

    tokenized = tokenizer.tokenizer(corrected_sentence)

    return tokenized
    

    



def normalize_accents(sentece: str) -> str:
    """Change whatever word with an accent to the ASCII version of the letter
    e.g: 
        'áÁ' ->'aA'
             
    """
    return unidecode.unidecode(sentece)


if __name__ == "__main__":
    print(text_normalization("hola que . , tall vámoss al cune hoy?"))