# Development


## Setup environment
Go to  query understanding folder
```bash
$ cd query-understanding
```

And then install the development dependencies:
```bash
$ pip install -r requirements.txt
```
<br></br>
## Run it
```bash
$ uvicorn main:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

```
<br></br>
## Notes

**Use the query-understanding folder as a root folder**, 
So if you want to try some nlp tools like spell_correction.py 
run like this:
```bash
$ python3 ./nlp_tools/spell_correction/spell_correction.py
```
<br></br>
## Unit Tests

To run all unit test in ./test/qu_test.py
```bash
python -m unittest ./test/qu_test.py
```

To run only one method of the class QueryUnderstandingTest in ./test/qu_test.py
```bash
python -m unittest test.qu_test.QueryUnderstandingTest.<test_method>
```

