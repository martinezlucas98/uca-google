
import numpy as np
import random

#probabilidad en el que se salta a unos de los links (para el pageRank)
DAMPING_FACTOR = 0.85

def calculate_backlinks(pages):
    """
        Calculamos los backlinks que tienen cada pagina.
    """
    
    for page in pages:
        backlinks = []
        for p in pages:
            if p != page:
                if page in pages[p]['links']:
                    backlinks.append(p)
        pages[page]['links'] = backlinks
    return pages
        

def generate_pages(indexes):
    """
        Generamos las paginas a buscar con sus backlinks correspondiente, se 
        retorna un diccionario donde las keys son las paginas y el valor otro
        diccionario con sus valores correspondiente para el retorno.
        Ej: {'url1':{'url':url1,'title':"t1", 'description':'d1', 'backlinks':[]}, 'url2': {...}, ...}
    """
    #se genera el dict
    indexes_keys = list(indexes.keys())
    linked_pages = {}
    for tk in indexes_keys:
        for page in indexes[tk]:
            linked_pages[page['url']] = {'title':page['title'], 
            'description':page['description'], 'links':page['links'], 'count':page['count']}
    linked_pages = calculate_backlinks(linked_pages)
    return linked_pages

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

def pagerank(indexes_pages, tol=0.001):
    """
        Damos un puntaje a cada pagina con el algoritmo pageRank.
        Retorna las paginas con sus puntuaciones, ej: {'page1':0.24342, 'page2':0.45346, ...}
    """
    PAGE_KEYS = indexes_pages.keys()
    # la puntuacion actual de las paginas, ej: {'page1':0.24342, 'page2':0.45346, ...}
    current_rank = {}
    for page in PAGE_KEYS:
        current_rank[page] = 1/len(PAGE_KEYS)
    
    #puntuacion actual para verficar la convergencia del pageRank
    prev_rank = current_rank.copy()
    while True:
        for current_page in PAGE_KEYS:                        
            prob = 0
            for page in PAGE_KEYS:
                page_links = indexes_pages[page]['links']
                # si no hay backlinks agregamos todas las paginas que tenemos
                if len(page_links) == 0:
                    page_links = PAGE_KEYS
                # la probabilidad de salir de nuestra pag. actual
                if current_page in page_links:
                    prob += prev_rank[page]/len(page_links)

            # aplicamos la formula del pageRank y actualizamos los puntajes,
            # probabilidad de seguir visitando paginas a partir de la actual
            prob = (1-DAMPING_FACTOR)/len(PAGE_KEYS) + DAMPING_FACTOR * prob
            current_rank[current_page] = prob

        #verificamos si las puntuaciones de las paginas convergen
        conv_total = 0            
        for page in prev_rank.keys():            
            if abs(prev_rank[page] - current_rank[page]) < tol:
                conv_total += 1
            else:
                break
        if conv_total == len(PAGE_KEYS):
            return current_rank
        #cargamos las punturacion actuales para seguir con la convergencia
        prev_rank = current_rank.copy()    
