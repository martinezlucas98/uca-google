
"""
*todo:
    @init(self, pages)
        En cada busqueda se debe generar los backlinks correctos para cada nodo,
        una optimizacion seria evitar esto ya sea busquedas semejantes en memoria, disco, etc.
        Actualmente se utiliza la interseccion de conjuntos de links de una pagina (page_link) con el total
        de links posibles para saber cuales descartar (total_link). 
        - Complejidad: 
            O(n*E)   con n>m  (caso promedio)
            O(n*m)    con  n<=m (peor de los casos)
        En Donde:
            n el número de páginas o nodos.
            m el número de links de cada página o número de hijos de cada nodo.
            E el numero de aristas del nodo actual
            
    @pagerank(self)
        Ejecuta el algoritmo con todos los metodos, en general el algoritmo inicial PageRank solo utiliza
        como metrica los backlinks entre cada pagina o nodo en nuestro caso, se podria agregar al peso como
        metrica de acuerdo al contenido de las paginas y mejorar la precision de la palabra a buscar.
        - Complejidad en cada iteracion:
            O(n*E)   (caso promedio)
            O(n*(n-1))  (peor de los casos)
        Donde:
            n el número de páginas o nodos.
            m el número de links de cada página o número de hijos de cada nodo.
            E el número de aristas.
    Para mas detalle leer el doc.
"""

import numpy as np
class GraphPageRank:
    """
        Algoritmo inicial del PageRank para medir la relevancia de cada pagina, utiliza como
        metrica solo los backlinks entre las paginas.

        *Artibutos:
            @nodes: dict{'url':{'children':[str], 'parents':[str], 'id' : int, 'score': float}, }
                Cada diccionario en el dict representa una pagina, y cada elemento
                del diccionario representa el contenido de la pagina con sus backlinks(children) a otra pagina, 
                parents las paginas que saltan a la pagina actual (el key url) y id su identificador y score su puntuacion.
            @damping_factor: float
                constante de amortiguacion libre de pageRank.
            @iteration: int
                el numero de iteraciones maximos, por defecto es 1000 que es una canitdad muy grande para el algoritmo pageRank
            @tol: float
                la tolerancia para saber la convergencia de las puntuaciones de las paginas.
    """
    def __init__(self, d=0.15, tol=0.001, it=1000):
        self.nodes = dict()
        self.__damping_factor = d
        self.__tol = tol
        self.__iteration = it

    def init(self, pages):
        """
        *Description:
            Se calcula los backlinks correctos de cada pagina y la agregamos la estructura de datos
            correspondiente a cada nodo.
            nodes: dict{'url':{'children':[str], 'parents':[str], 'id' : int, 'score': float}, }
        *Parameters
            @pages: dict{'page_id':{'url':str, 'title':str, 'description':str, 'content':str},...}
                contiene el total de paginas donde aparecen los tokens,
                donde cada id del diccionario representa otro dict que contiene la informacion de
                la pagina.
        *Returns
            None
        """
        # cada pagina 'url' sera un nodo
        for page_id in pages:
            page = pages[page_id]['url']
            self.nodes[page] = {'children': set(pages[page_id]['links']), 'parents': [], 'id': page_id, 'score': 1.0}

        # generamos los backlinks de cada nodo
        for page in self.nodes.keys():
            # la interseccion de ambos conjuntos son los backlinks (children) correctos para cada nodo
            backlinks = self.nodes.keys() & self.nodes[page]['children']
            self.nodes[page]['children'] = list(backlinks)
            # con los nuevos hijos actualizamos los padres correspondientes
            for link in backlinks:
                #self.nodes[link]['parents'].add(page)
                self.nodes[link]['parents'].append(page)
    
    def update_score(self, page):
        """
        *Description:
            Actualiza la puntuacion de una pagina, la puntuacion nueva sera la probabilidad
            de quedarse o no en la pagina actual.
        *Parameters:
            @page: str
                la url o nombre de la pagina a actualizar.
        *Returns:
            None
        """
        # cada nodo padre del nodo page es su vecino, por lo que actualizamos la 
        # probabilidad de visitar uno de sus hijos (el node page es uno de ellos).
        score_sum = 0.0
        for parent in self.nodes[page]['parents']:
            score_sum += self.nodes[parent]['score'] / len(self.nodes[parent]['children'])
        # luego actualizamos la probabilidad de salir de nuestra pag. actual
        pagerank = self.__damping_factor / len(self.nodes) + (1-self.__damping_factor) * score_sum
        # actualizamos la puntuacion
        self.nodes[page]['score'] = pagerank

    def normalize_pagerank(self):
        """
        *Description:
            actualizamos las punturaciones de cada pagina, donde en cada normalizacion
            puntuamos que tan probable es visitar una pagina "x", mediante mas alto sea
            la probabilidad es mejor, luego se chequea si con la nueva actualizacion de 
            puntuaciones hubo convergencia.
        *Parameters:
            @self
        *Returns:
            @boolean
            True si la puntuacion convergen false en caso contrario
        """
        # sumamos el total de puntuaciones
        score_sum = sum(self.nodes[page]['score'] for page in self.nodes)
        # normalizamos la puntuacion de cada pagina, si converge quiere decir
        # que pagerank_sum = 1.0 para la tolerancia aplicada (por defecto tol=0.001)
        conv_total = 0
        for page in self.nodes:
            prev_score = self.nodes[page]['score']
            self.nodes[page]['score'] /= score_sum
            # verficamos la convergencia
            if abs(prev_score - self.nodes[page]['score']) < self.__tol:
                conv_total +=1
        # verificamos is todas las pagina convergen
        return conv_total == len(self.nodes.keys())
                
    def sort(self):
        """
            Ordena el contenido el resultado por relevancia, en orden decreciente.
        """
        self.nodes = dict(sorted(self.nodes.items(), key=lambda x: x[1]['score'], reverse=True))
    
    def pagerank(self):
        """
        *Description:
            En cada iteracion actualizamos o normalizamos las puntuaciones de cada nodo hasta
            que convergan o hasta que se cumpla las "n" iteraciones.
        *Parameters:
            @self
        *Returns:
            None
        """
        # por defecto iteration = 1000 que es una cantidad muy grande para el algoritmo pageRank
        for i in range(self.__iteration):
            for page in self.nodes:
                self.update_score(page)
            # actualizamos la puntuacion de todas las paginas y verificamos la convergencia
            is_convergent = self.normalize_pagerank()
            if is_convergent:
                break
    
    def get_results (self, pages):
        """
        *Description:
            Se obtiene el resultado url, title y descripcion de cada pagina, de acuerdo al ordenamiento
            de los nodos.
        *Parameters
            @pages: dict{'page_id':{'url':str, 'title':str, 'description':str, 'content':str},...}
                contiene el total de paginas donde aparecen los tokens,
                donde cada id del diccionario representa otro dict que contiene la informacion de
                la pagina.
        *Returns
            @results: list[dict{'url':str, 'title':str, 'description':str}]
                Cada diccionario en la lista representa una pagina, y cada elemento
                del diccionario representa el contenido de la pagina.
        """     
        results = []
        # cada nodo es un dict{'url':{'children':[str], 'parents':[str], 'id' : int, 'score': float}, }
        for page in self.nodes:
            # el id de la pagina que contiene toda la informacion de la pagina
            page_id = self.nodes[page]['id']
            description = pages[page_id]['content']
            description = description[:300]      
            results.append(
                {
                    "url": pages[page_id]['url'],
                    "title": pages[page_id]['title'],
                    "description": description
                }
            )
        return results

        