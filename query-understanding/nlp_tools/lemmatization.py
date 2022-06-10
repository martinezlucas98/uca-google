import spacy

def lemmatizer(words: list, lang='es')-> list:
    """Give a list of words 
    and return a list of lemmatized words 

    Lemmatization - The transformation that uses a dictionary to map a word’s variant back to its root format

    e.g:
     tokenizer(['haciendo','tarea'] )
     -> ['hacer', 'tarea']
     where 'hacer' is the root format of 'haciendo'
    """
    
    sentence = (' ').join(words)
    
    if lang == "en":
        nlp = spacy.load('en_core_web_sm')
    else:
        nlp = spacy.load('es_core_news_sm')
    doc = nlp(sentence)
    lemmatized = [w.lemma_ for w in doc]
    return lemmatized

if __name__ == '__main__':
    print(lemmatizer(['doing','tarea', 'hablamos'], 'en' ))
