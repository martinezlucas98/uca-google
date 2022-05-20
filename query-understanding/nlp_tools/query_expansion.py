from cgitb import text
from ntpath import join
import numpy as np
import logging
from numpy.linalg import norm
from gensim.models import KeyedVectors

#logging.basicConfig(format='%(asctime)s : %(message)s', level=logging.INFO)
we = KeyedVectors.load_word2vec_format('nlp_tools/fasttext-sbwc.100k.vec', limit=100000)
#we = KeyedVectors.load_word2vec_format('fasttext-sbwc.100k.vec', limit=100000)
clases = []
#Conjunto de clases que usamos para clasificar el query
with open('nlp_tools/clases.tsv') as f:
#with open('clases.tsv') as f:
    clases = [line[:-1] for line in f]

#Query expansion
def query_expansion(texto):
  #return we.similar_by_word("mujer")
  words_exp = []
  for word in texto:
    if word in we:
      words_exp += we.most_similar(positive=word)
  final = [ x[0] for x in words_exp]
  return final
    

#Reconocimiento de entidad
def classification(texto, clases):
  sims = [similarity(texto, clase) for clase in clases]
  indices = range(len(sims))
  ind_max = max(indices, key=lambda i: sims[i])
  return ind_max

def to_vector(texto):
  tokens = texto.split()
  vec = np.zeros(300)
  for word in tokens:
    # si la palabra está la acumulamos
    if word in we:
        vec += we[word]
  return vec / norm(vec)

def similarity(texto_1, texto_2):
  vec_1 = to_vector(texto_1)
  vec_2 = to_vector(texto_2)
  sim = vec_1 @ vec_2
  return sim

def entity_recongnition(texto):
  return clases[classification(texto,clases)]
  
#print(entity_recongnition(['cuarto','de','pollo']))
#print("\nquery expansion: ",query_expansion(['mujer','tesis','feliz']))
#print(we.most_similar(positive=['rey','mujer'], negative=['hombre']))
