# Endpoints
## /expand_query?q='sentence'
|  Path          |     Query    |    Method | Description | 
| -------------  | -------------| --------- | --------- |
| /expand_query  | q: String    |    GET    |  returns the structured 'sentence' with the attributes listed below    |

### Example
```bash
$ curl -X 'GET' 'http://127.0.0.1:8081/expand_query?q=horarios%20de%20clase%3F%3F%3F%3F' -H 'accept: application/json'
```
```python
q = 'horarios de clase????'
```
Response:
```json
{
  "status": "ok",
  "original_sentence": "horarios de clase????",
  "corrected_sentence": "horarios de clase",
  "language": "spanish", //For now it is a static value
  "lemmatized_tokens": [
    "horario",
    "clase"
  ],
  "stemmed_tokens": [
    "horari",
    "clas"
  ],
  "query_expansion": [
    "horario",
    "horarias",
    "festivos",
    "horaria",
    "sábados",
    "feriados",
    "descansos",
    "itinerarios",
    "domingos",
    "trayectos",
    "la",
    "y",
    "</s>",
    "en",
    "del",
    "el",
    "0",
    "los",
    "las",
    "incluyendo",
    "clases",
    "subclase",
    "subclases",
    "acomodada",
    "class",
    "trabajadora",
    "adinerada",
    "obrera",
    "destructores",
    "pudiente"
  ],
  "classification": "ropa de vestir" // needs a little fix here 😶
}
```
<br>

## /autocomplete?q='sentence'

### Still in development🧑‍💻 👩‍💻

<br>


# Setup environment
Go to  query understanding folder
```bash
$ cd query-understanding
```

Create a virtual environment 'env'
```bash
$ python -m venv env
```

Activate virtual environment
```bash
$ source ./env/bin/activate
```

And then install the development dependencies:
```bash
$ pip install -r requirements.txt
```

<br>

# Run it
```bash
$ uvicorn main:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

```

or if you want to change the port like 8081
```bash
$ uvicorn main:app --host 127.0.0.1 --port 8081
```
<br></br>
# Notes

**Use the query-understanding folder as a root folder**, 
So if you want to try some nlp tools like spell_correction.py 
run like this:
```bash
$ python3 ./nlp_tools/spell_correction/spell_correction.py
```
<br></br>
# Unit Tests

To run all unit test in ./test/qu_test.py
```bash
python -m unittest test.qu_test
```

To run only one method of the class QueryUnderstandingTest in ./test/qu_test.py
```bash
python -m unittest test.qu_test.QueryUnderstandingTest.<test_method>
```

