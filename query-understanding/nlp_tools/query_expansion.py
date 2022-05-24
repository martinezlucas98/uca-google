from cgitb import text
from ntpath import join
from urllib import response
import numpy as np
from numpy.linalg import norm
from gensim.models import KeyedVectors
import requests
import os

import zlib


VECT_URL = 'http://dcc.uchile.cl/~jperez/word-embeddings/fasttext-sbwc.100k.vec.gz'


if not os.path.exists('dataset/fasttext-sbwc.100k.vec'):
  print("Downloading fasttext-sbwc.100k.vec.gz ......")
  print("This should only happen once")
  response = requests.get(VECT_URL)
  data = zlib.decompress(response.content, zlib.MAX_WBITS|32)
  with open('dataset/fasttext-sbwc.100k.vec','wb') as outFile:
    outFile.write(data)


we = KeyedVectors.load_word2vec_format('dataset/fasttext-sbwc.100k.vec', limit=100000)
clases = []
with open('dataset/clases.tsv') as f:
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
  final = [ x[0] for x in words_exp]
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
  """Give a list of words 
    and convert the list of words to a vector, 
    add the vectors, and then return the resulting normalized vector
  """
  tokens = texto.split()
  vec = np.zeros(300)
  for word in tokens:
    if word in we:
        vec += we[word]
  return vec / norm(vec)

def similarity(texto_1, texto_2):
  """Given two sentences 
    and find the similarity of texts, 
    using vectors and dot product of numpy

    e.g:
      similarity('perro','perros')
        -> '0.95'
  """
  vec_1 = to_vector(texto_1)
  vec_2 = to_vector(texto_2)
  sim = vec_1 @ vec_2
  return sim

def entity_recongnition(texto):
  """Give a sentence 
    and returns the entity of the sentence 

    e.g:
      entity_recongnition('un cuarto de pollo')
        -> 'alimentos'
  """
  return clases[classification(texto,clases)]
