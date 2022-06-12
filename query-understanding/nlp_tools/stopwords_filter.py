import nltk
nltk.download('stopwords')
import datetime
from nltk.corpus import stopwords

STOPWORDS_ES = set(stopwords.words('spanish'))

def remove_stopwords(words: list) -> list:
    
    start_time = datetime.datetime.now()


    no_stopwords = [ w  for w in words if w not in STOPWORDS_ES]

    end_time = datetime.datetime.now()
    time_diff = (end_time - start_time)
    execution_time = time_diff.total_seconds() * 1000
    print("execution time in remove_stopwords",execution_time, "ms")

    return no_stopwords

    

if __name__ == "__main__":
    print(remove_stopwords(['hola', 'yo', 'dia', 'Día','soy', 'de','mi','la', 'perro', 'gato', 'tarea', 'horario']))
