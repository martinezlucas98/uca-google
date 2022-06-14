
import numpy as np
import random
from copy import deepcopy

class PageRank:
    """
        Algoritmo inicial del PageRank para medir la relevancia de cada pagina, utiliza como
        metrica solo los backlinks entre las paginas.

        *Artibutos:
            @pages: dict{'page_id':{'url':str, 'title':str, 'description':str, 'content':str},...}
                contiene el total de paginas donde aparecen los tokens,
                donde cada id del diccionario representa otro dict que contiene la informacion de
                la pagina.
            @indexes_pageRank: dict{'url':{'links':[str], 'id' : int,'score': float}, }
                Cada diccionario en el dict representa una pagina, y cada elemento
                del diccionario representa el contenido de la pagina con sus links a otra pagina
                perteneciente a pages, id su identificador y score su puntuacion.
            @damping_factor: float
                constante de amortiguacion libre de pageRank.
            @iteration: int
                el numero de iteraciones maximos.
            @tol: float
                la tolerancia para saber la convergencia de las puntuaciones de las paginas.

    """  
    def __init__(self, indexes, d=0.85, tol=0.001, it = 1):
        self.__pages = indexes['pages']
        self.__indexes_pageRank = {}
        self.__damping_factor = d
        self.__tol = tol
        self.__iteration = it        
        self.__generate_pages(indexes['tokens'])
    
    def get_indexes_pageRank(self):
        """
            Metodo get, solo para el test.
        """
        return self.__indexes_pageRank

    def __generate_pages(self, tokens):
        """
        *Description:
            Se calcula los backlinks correctos de cada pagina y la agregamos a nuestra estructura
            de dato para el rankeo.
        *Parameters
            @tokens: str
                Los tokens de la palabra tokenizada, ej: 'La universidad catolica' -> ['universi', 'catolic']
        *Returns
            @results: dict{'url1':{'links':list[], 'id':int, 'score':float}}
                Cada diccionario en el dict representa una pagina, y cada elemento
                del diccionario representa el contenido de la pagina para la puntuacion correcta.
        """    
        for token in tokens:
            for page_id in tokens[token]:
                try:
                    page_url = self.__pages[page_id]['url']
                except Exception as err:
                    continue
                self.__indexes_pageRank [page_url] = {'links':[], 'id' : page_id,'score': 1.0}
                # self.__indexes_pageRank [page_url] = {'links':self.__pages[page_id]['links'], 'id' : page_id,'score': 1.0}
        
        for page in self.__indexes_pageRank:
            for page_id in self.__pages:
                if (self.__indexes_pageRank[page]['id'] != page_id):
                    if(page in self.__pages[page_id]['links']):
                        page_url = self.__pages[page_id]['url']
                        index_url = self.__indexes_pageRank[page_url]
                        index_url['links'].append(page)                    
        
    def sort(self):
        """
            Ordena el contenido el resultado por relevancia, en orden decreciente.
        """
        self.__indexes_pageRank = dict(sorted(self.__indexes_pageRank.items(), key=lambda x: x[1]['score'], reverse=True))

    def get_results(self):
        """
        *Description:
            Se obtiene el resultado actual de __indexes_pageRank con los datos de 
            url, title y descripcion de cada pagina.
        *Parameters
            @self
        *Returns
            @results: list[dict{'url':str, 'title':str, 'description':str}]
                Cada diccionario en la lista representa una pagina, y cada elemento
                del diccionario representa el contenido de la pagina.
        """ 
        results = []
        for page in self.__indexes_pageRank:
            page_id = self.__indexes_pageRank[page]['id']
            description = self.__pages[page_id]['content']
            description = description[:300]
            result = {
                'url': page,
                'title': self.__pages[page_id]['title'],
                'description': description, 
            }
            results.append(result)
        
        return results

    def rank_pages(self):
        """
            Damos un puntaje a cada pagina con el algoritmo pageRank, para poder medir la relevancia
            de cada pagina, se puntua hasta la convergencia o hasta llegar el limite de iteraciones.
        """
                
        # la puntuacion actual de las paginas, ej: 'url1':{'links':[...], 'id' : 1,'score': 0.4567}, ...
        for page in self.__indexes_pageRank.keys():            
            self.__indexes_pageRank [page]['score'] /= len(self.__indexes_pageRank.keys())
                    
        #puntuacion actual para verficar la convergencia del pageRank        
        prev_rank = deepcopy(self.__indexes_pageRank)

        # numero de paginas que convergen
        conv_total = 0
        # contador de la iteracion
        it = 0
        while (conv_total != len(self.__indexes_pageRank.keys()) and it < self.__iteration):
            # cada current_page es el identificador de la pagina actual, ej: 12,33,1, etc
            for current_page in self.__indexes_pageRank.keys():                        
                prob = 0
                # cada page, es la url de la pagina
                for page in self.__indexes_pageRank.keys():
                    # se obtiene todos los links vinculados de la pagina
                    page_links = self.__indexes_pageRank[page]['links']
                    # si no hay backlinks agregamos todas las paginas que tenemos
                    if len(page_links) == 0:
                        page_links = self.__indexes_pageRank.keys()
                    # la probabilidad de salir de nuestra pag. actual
                    if current_page in page_links:                                                
                        prob += prev_rank[page]['score']/len(page_links)
                # aplicamos la formula matematica del pageRank y actualizamos la puntuacion de la pagina actual
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
