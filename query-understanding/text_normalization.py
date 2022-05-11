from tokenize import String
from nlp_tools.spell_correction import spell_correction

def text_normalization(sentence: str):
    #sentence = normalize_accents(sentence: str) -> str

    words_corrected = [spell_correction.correction(word) for word in sentence.split()]
    corrected_sentence = ' '.join(words_corrected)
    print(corrected_sentence)
    



def normalize_accents(sentece: str) -> str:
    """Change whatever word with an accent to the ASCII version of the letter


    e.g: 
        'áÁ' ->
             
    """
    pass


if __name__ == "__main__":
    print(text_normalization("hola que tall vamoss al cune hoy?"))