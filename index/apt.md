# Acceptance Test Plan
24/05/2022

## Goal
- Basic indexing and index serving
- Integration with other modules (online serving and crawler)

## Features
| Submodule | Functionality                                           | Implemented | Tested |
| --------- | ------------------------------------------------------- | ----------- | ------ |
| Indexer   | Read & process crawler output                           | Yes         | Yes    |
| Indexer   | Index page updates                                      | Yes         | Yes    |
| Indexer   | Index serialization and saving                          | Yes         | Yes    |
| Indexer   | Index categorization, multiple indices                  | No          | -      |
| Indexer   | Store page title, description and backlinks             | Yes         | Yes    |
| Indexer   | Word normalization and punctuation removal for indexing | Yes         | Yes    |
| Indexer   | Categorize words (word type, topic, language, etc.)     | No          | -      |
| Server    | Search by substrings and starting string                | Yes         | Yes    |
| Server    | Search by synonym                                       | No          | -      |
| Server    | Search by topic                                         | No          | -      |

<!-- Sugerencias (no es parte de la 2da entrega pero para tener en cuenta para la siguiente)
Script(s) para levantar todo el sistema de forma mas facil, para no ir a cada modulo a correr un comando diferente
Definir puertos para cada servicio, no me gusta que el index_server use 8080 por ej.
Indexer: Indexar palabras del title, no se indexan actualmente
         Optimizar guardado de informacion de paginas, hay demasiada redundancia y se infla el indice
Server: paginas con multiples palabras. AND en vez de OR. Tal vez es mas tarea del online serving
Online serving: pagerank parece priorizar paginas con muchos links demasiado
 -->