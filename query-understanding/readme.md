# Endpoints

|  Path          |     Query    |    Method | Description | 
| -------------  | -------------| --------- | --------- |
| /expand_query  | q: String    |    GET    |  returns the structured 'sentence' with the attributes listed below    |
| /autocomplete  | q: String    |    GET    |  return a list of a autocompletes options.  |
| /lemmastemm    | q: String    | GET       | A 'lighter' and faster version of /expand_query, which returns only the language, lammatization and stemming.
### Example for  /expand_query
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

<br>

# Latest improvements (22/06/2022)
- New Language Support: English.

- Improve Spanish Detection.
- Improve performance in some modules like lemmatization, stemming, tokenizer and lang_detect. Loading heavy objects into memory only once when starting the service and not every time these modules are used.
- Two new Api Routes:<br>
<span style="margin-left: 10px">
    <b>/autocomplete</b>:  returns the same autocomplete options that google scholar returns.
</span><br>
<span style="margin-left: 10px">
    <b>/lemmastemm</b>:  A 'lighter' and faster version of <b>/expand_query</b>, which returns only the language, lammatization and stemming.
</span>

<br>

# Issues
- The New Lang_detect2 module is more precise when detecting the Spanish language but it increases the response time quite a bit

- Most of the modules that have  <b>/expand_query</b> and <b>/lemmastemm</b> in common have a pretty good performance (between 1 to 5 ms), while the <b>lemmatization</b> module takes between 40ms to 200ms, so it would be nice to improve the lemmatization time.

- The <b>classification</b> module Sometimes does not return the desired value, since the data set is minimal, that is, it contains very few words, more words need to be added in order to give greater results.
Example for the argument "schedules" the classification "bus" is returned which may make sense but if we ask for "class schedules" it returns "dress clothes"

# Ideas for future development
- Work with the index service to get autocomplete answers based on the UC Google environment.
- Save autocomplete history.
- Build Machine Learning models to classify the query.


