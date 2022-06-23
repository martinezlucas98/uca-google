import spacy
import datetime


nlp_english = spacy.load('en_core_web_sm')
nlp_spanish = spacy.load('es_core_news_sm')

def lemmatizer(words: list, lang='es')-> list:
    """Give a list of words 
    and return a list of lemmatized words 

    Lemmatization - The transformation that uses a dictionary to map a word’s variant back to its root format

    e.g:
     tokenizer(['haciendo','tarea'] )
     -> ['hacer', 'tarea']
     where 'hacer' is the root format of 'haciendo'
    """
    start_time = datetime.datetime.now()
    sentence = (' ').join(words)
    
    if lang == "en":
        doc = nlp_english(sentence)
    else:
        doc = nlp_spanish(sentence)

    lemmatized = [w.lemma_ for w in doc]

    end_time = datetime.datetime.now()
    time_diff = (end_time - start_time)
    execution_time = time_diff.total_seconds() * 1000
    print("execution time in lemma",execution_time, "ms")
    return lemmatized

if __name__ == '__main__':
    print(lemmatizer(['doing','tarea', 'hablamos'], 'es' ))
