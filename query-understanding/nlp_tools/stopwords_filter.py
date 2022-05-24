import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

STOPWORDS_ES = set(stopwords.words('spanish'))

def remove_stopwords(words: list) -> list:
    
    no_stopwords = [ w  for w in words if w not in STOPWORDS_ES]
    return no_stopwords

    

if __name__ == "__main__":
    print(remove_stopwords(['hola', 'yo', 'dia', 'Día','soy', 'de','mi','la', 'perro', 'gato', 'tarea', 'horario']))
