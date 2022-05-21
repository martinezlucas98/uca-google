from cgitb import text
from ntpath import join
import numpy as np
import logging
from numpy.linalg import norm
from gensim.models import KeyedVectors
from sklearn.metrics import classification_report, accuracy_score
from zmq import NULL

we = KeyedVectors.load_word2vec_format('nlp_tools/fasttext-sbwc.100k.vec', limit=100000)
clases = []
with open('nlp_tools/clases.tsv') as f:
  clases = [line[:-1] for line in f]

#Query expansion
def query_expansion(texto):
  """Give a list of words 
    and return a list of related words 

    Query expansion - Add related words to a query in order to increase the number of returned documents and improve recall accordingly.

    e.g:
     query_expansion(['tesis','del','año','2019] )
     -> ['doctoral', 'teoria','disertacion']
  """
  words_exp = []
  for word in texto:
    if word in we:
      words_exp += we.most_similar(positive=word)
  final = [ x[0] for x in words_exp[0:10]]
  return final
    
#Classification of sentence
def classification(texto, clases):
  """Give a sentence 
    and returns the classification group of the sentece

    e.g:
     classification('cuarto de pollo')
     ->  'alimentos'
  """
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
