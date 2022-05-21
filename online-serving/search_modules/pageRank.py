
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
            linked_pages[page['url']] = {'url':page['url'],'title':page['title'], 
            'description':page['description'], 'links':page['links']}
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

def pagerank(indexes_pages, n=1000):
    """
        Retorna un diccionario donde las keys son las puntuaciones asociado con
        cada pagina, n es n-iteraciones suficientes para poder 
        converger los valores rankeados.
    """
    indexes_pages = generate_pages(indexes_pages)
    # comenzamos en una pagina aleatoria
    page = random.choice(list(indexes_pages.keys()))
    # contendra todas las posibles paginas a visitar a partir de la pag. actual
    # para luego poder rankear.
    visited = []
    visited.append(page)
    
    # agregamos a visitados todas las posibles paginas que visitaremos a partir de la actual
    # logicamente habra mas de uno.
    for i in range(n):        
        probabilities = get_next_page_prob(indexes_pages, visited[i])
        next_page = np.random.choice(list(probabilities.keys()), p=list(probabilities.values()))
        # agregamos la siguiente pagina posible a visitar
        visited.append(next_page)
    
    #rankeamos las paginas
    ranked_pages = {}
    for page in indexes_pages.keys():
        rank = visited.count(page)/len(visited)
        ranked_pages[rank] = indexes_pages[page]
    #odernamos de acuerdo a la puntuacion
    ranked_pages = dict(sorted(ranked_pages.items(), reverse=True))
 
    return ranked_pages
