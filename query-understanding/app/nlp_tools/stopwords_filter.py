# import spacy
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

STOPWORDS_ES = set(stopwords.words('spanish'))

def remove_stopwords(words: list) -> list:
    
    # nlp = spacy.load('es_core_news_sm')
    
    # filtered_sentence =[] 
    # for word in words:
    #     lexeme = nlp.vocab[word]
    #     if lexeme.is_stop == False:
    #         filtered_sentence.append(word) 
    
    # return filtered_sentence
   
    no_stopwords = [ w  for w in words if w not in STOPWORDS_ES]
    return no_stopwords

    

if __name__ == "__main__":
    print(remove_stopwords(['hola', 'yo', 'dia', 'Día','soy', 'de','mi','la', 'perro', 'gato', 'tarea', 'horario']))
