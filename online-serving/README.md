# Online-serving
## Requirements:
###Dependencies
Install the development dependencies:
```bash
$ pip install -r requirements.txt
```
or follow the manual installation in case of problems.
### Manual installation
#### fastAPI Framework
For launch our HTTP services we use the fastAPI framework.
Run it:
```bash
$ pip install fastapi
$ pip install "uvicorn"
```
more info: https://fastapi.tiangolo.com/#installation
####NLTK
For query tokenization, the nltk modules are used.
Run it:
```bash
$ pip3 install nltk
$ python3 -m nltk.downloader popular
```
more info: https://www.nltk.org/install.html
###INDEXES
For indexes, the HTTP services of the index module are required.
See documentation: https://github.com/martinezlucas98/uca-google/tree/index/index#readme

## Running online-serving
From the project root:
```bash
$ uvicorn main:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

```
And then run index server: https://github.com/martinezlucas98/uca-google/tree/index/index#readme
