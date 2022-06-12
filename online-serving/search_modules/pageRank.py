
import numpy as np
import random
from copy import deepcopy

def get_next_page_prob(indexes_pages, current_page):
    """
        Retorna una distribución de probabilidad sobre qué página visitar a continuación,
        a partir de la pagina actual, donde el key es la pagina y el valor es la probabilidad
        de que sea la siguiente pagina a visitar.
    """
    # calculamos la prob. de visitar cualquier otra pagina aleatoria, si la pagina actual no tiene
    # links a otras paginas directamente sabemos que se visitara cualquier otra pagina en caso contrario
    # debemos saber que tan probable es visitar una pagina mediante links enlazados o ir directamente
    # a otra pagina (sin links).
    probability = {}
    if len(indexes_pages[current_page]['links']) == 0:
        #si no tenemos ningun otro link se visita cualquier otra pagina
        prob_page = 1/len(indexes_pages.keys())
    else:
        #prob. de cuando se visita directamente otra pagina (sin los links)
        prob_page = (1-DAMPING_FACTOR)/len(indexes_pages.keys())
        #prob. de seguir visitando paginas mediante los links
        prob_link = DAMPING_FACTOR/len(indexes_pages[current_page]['links'])

    #cargamos una distribucion de posibilidades de que pagina visitar de todas las posibles        
    for page in indexes_pages.keys():
        if page in indexes_pages[current_page]['links']:
            probability[page] = prob_page + prob_link
        else:
            probability[page] = prob_page
                                                
    return probability

class PageRank:
    def __init__(self, indexes, d=0.85, tol=0.001, it = 1):
        self.__pages = indexes['pages']
        self.__indexes_pageRank = {}
        self.__damping_factor = d
        self.__tol = tol
        self.__iteration = it        
        self.__generate_pages(indexes['tokens'])
            
    def __generate_pages(self, tokens):
        for token in tokens:
            for page_id in tokens[token]:
                page_url = self.__pages[page_id]['url']
                # self.__indexes_pageRank [page_url] = {'links':[], 'id' : page_id,'score': 1.0}
                self.__indexes_pageRank [page_url] = {'links':self.__pages[page_id]['links'], 'id' : page_id,'score': 1.0}
        
        for page in self.__indexes_pageRank:
            for page_id in self.__pages:
                if (self.__indexes_pageRank[page]['id'] != page_id):
                    if(page in self.__pages[page_id]['links']):
                        page_url = self.__pages[page_id]['url']
                        index_url = self.__indexes_pageRank[page_url]
                        index_url['links'].append(page)                    
        
    def sort(self):
        self.__indexes_pageRank = dict(sorted(self.__indexes_pageRank.items(), key=lambda x: x[1]['score'], reverse=True))

    def get_results(self):
        results = []
        for page in self.__indexes_pageRank:
            page_id = self.__indexes_pageRank[page]['id']
            result = {
                'url': page,
                'title': self.__pages[page_id]['title'],
                'description': self.__pages[page_id]['description'], 
            }
            results.append(result)
        
        return results

    def pagerank(self):
        """
            Damos un puntaje a cada pagina con el algoritmo pageRank.
            Retorna las paginas con sus puntuaciones, ej: {'page1':0.24342, 'page2':0.45346, ...}
        """
                
        # la puntuacion actual de las paginas, ej: {'page1':0.24342, 'page2':0.45346, ...}        
        for page in self.__indexes_pageRank.keys():            
            self.__indexes_pageRank [page]['score'] /= len(self.__indexes_pageRank.keys())
                    
        #puntuacion actual para verficar la convergencia del pageRank        
        prev_rank = deepcopy(self.__indexes_pageRank)
     
        conv_total = 0
        it = 0
        while (conv_total != len(self.__indexes_pageRank.keys()) and it < self.__iteration):        
            for current_page in self.__indexes_pageRank.keys():                        
                prob = 0
                for page in self.__indexes_pageRank.keys():
                    page_links = self.__indexes_pageRank[page]['links']
                    # si no hay backlinks agregamos todas las paginas que tenemos
                    if len(page_links) == 0:
                        page_links = self.__indexes_pageRank.keys()
                    # la probabilidad de salir de nuestra pag. actual
                    if current_page in page_links:                                                
                        prob += prev_rank[page]['score']/len(page_links)
                
                prob = (1 - self.__damping_factor) / len(self.__indexes_pageRank.keys()) + self.__damping_factor * prob                
                self.__indexes_pageRank[current_page]['score'] = prob
            #verificamos si las puntuaciones de las paginas convergen
            conv_total = 0            
            for page in prev_rank.keys():
                rank = abs(prev_rank[page]['score'] - self.__indexes_pageRank[page]['score'])                
                if rank < self.__tol:
                    conv_total += 1
                else:
                    break         
            #cargamos las punturacion actuales para seguir con la convergencia            
            prev_rank = deepcopy(self.__indexes_pageRank)         
            it += 1   
