import spacy

def get_entity(sentence: str) -> dict:
    nlp = spacy.load("es_core_news_sm")
    doc = nlp(sentence)

    text_entity = {}

    for ent in doc.ents:
        text_entity[ent.text] = ent.label_

    return text_entity

if __name__ == "__main__":
    print(get_entity("apple compra muchas cosas y Samsung no" ))