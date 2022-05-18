import spacy

def get_part_of_speech(sentence: str) -> dict: 
    nlp = spacy.load("es_core_news_sm")
    doc = nlp(sentence)

    response = {}
    for token in doc:
        response[token.text] = token.pos_

    return response

   
if __name__ == "__main__":
    print(get_part_of_speech("steve jobs fallece el 5 de octubre"))

##Apple is looking at buying U.K. startup for $1 billion"

 # for token in doc.ents:
    #     print(token.text, '->', token.label_)