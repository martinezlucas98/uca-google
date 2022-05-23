# Online-serving
This service is responsible for scoring the search pages to rank it by relevance to return as search result.
## Getting Started
These instructions are necessary to be able to run the necessary services of the project on your local machine.
### Prerequisites
First make sure that the query-undestanding and index services respond correctly on the local machine.
- For indexes, the HTTP services of the index module are required.
See documentation: https://github.com/martinezlucas98/uca-google/tree/index/index#readme
- For query tokenization, the HTTP services of the query-understanding module are required.
See documentation: https://github.com/martinezlucas98/uca-google/tree/query-understanding/query-understanding#readme

For our service, first create a virtual environment for python, you can use your own virtual environment. 
For this guide I will use [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) (with [Anaconda](https://www.anaconda.com/products/distribution)).
To create an environment:
```bash
$ conda create --name online-serving python=3.9
```
To activate this environment, use:
```bash
$ conda activate online-serving
```

### Installing
Install the development dependencies:
```bash
$ pip install -r requirements.txt
```
or follow the manual installation in case of problems.
### Manual installation
The necessary packages are listed:
#### Requests
Request is a simple HTTP library for Python.
You can install requests with:
```bash
$ pip install requests
```
#### fastAPI Framework
For launch our HTTP services we use the fastAPI framework.
You can install fastApi with:
```bash
$ pip install fastapi
$ pip install "uvicorn"
```
more info: https://fastapi.tiangolo.com/#installation
#### NumPy
This fundamental package for scientific computing with Python is used for ranking pages by relevance.
 You can install NumPy with:
 ```bash
$ pip install numpy
```
#### NLTK
For query tokenization, the nltk modules are used.
You can install NLTK with:
```bash
$ pip install nltk
$ python -m nltk.downloader popular
```
more info: https://www.nltk.org/install.html

## Running online-serving
In settings.py, you must define the assigned ports for services Index and query-understanding:
```py
# SERVER (config)
## host
HOST = "http://localhost"
## port
PORT_INDEX = "8080" #port for index
PORT_QUERY = "8081" #port for query understanding

#PATH (no config)
PATH_INDEX = HOST + ":" + PORT_INDEX + "/"
PATH_QUERY = HOST + ":" + PORT_QUERY + "/"
```
modifies the ports with the value assigned for services index and query-understanding. Do not modify the PATH.

Check the connection with the other services:
```bash
$ python -m unittest -v service_test.ServiceTest

test_index_service (service_test.ServiceTest) ... ok
test_query_service (service_test.ServiceTest) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.004s

OK
```
If there are errors or failures in the test result, check the assigned ports correctly.

From the project root:
```bash
$ uvicorn main:app --host 127.0.0.1 --port 8000 --reload 

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

```
