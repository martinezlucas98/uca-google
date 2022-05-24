"""
    Archivo de configuraciones
"""

# SERVER (config)
## host
HOST = "http://localhost"
## port
PORT_INDEX = "8080" #port for index
PORT_QUERY = "8081" #port for query understanding
PORT_ONLINE = "8000" #port for my service

#PATH (no config)
PATH_INDEX = HOST + ":" + PORT_INDEX + "/"
PATH_QUERY = HOST + ":" + PORT_QUERY + "/"
PATH_ONLINE = HOST + ":" + PORT_ONLINE + "/"