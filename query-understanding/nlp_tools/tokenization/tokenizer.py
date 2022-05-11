import spacy
import pickle



def tokenizer(sentence: str)-> list:
    """Give a sentence 
    this function separate the sentence in units called 'tokens'

    where a token can be a word or some '.', '!', '?' ',', etc..

    e.g:
     tokenizer('hola que tal!.')
     -> ['hola', 'que', 'tal', '!', '.']
     wehere in the list the 'hola' is a token and 'que' is another token
    """
    nlp = spacy.load('es_core_news_sm')
    doc = nlp(sentence)
    print(doc.text)
    print([(w.text, w.pos_) for w in doc])


if __name__ == '__main__':
    tokenizer('haciendo que tal amigos... ')