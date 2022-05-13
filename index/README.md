<!--
## TODO
- [ ] Unit tests
Indexes:
    URLs to pages needed
- [ ] Puctuation stripped
- [ ] Punctuation included
- [ ] Multiple words (?)
- [ ] URL to title and meta tags/descriptions
Updates:
    Calculate a hash of a page's content when indexing, for updates check hashes to see if it's worth
    going through and reindexing the page.
Page rank:
    Calculate ranking based on backlinks, counts, etc
    Retrieval date

## Notes
string punctuation: word_data.translate(word_data.maketrans('', '', string.punctuation + '…°'))
strip accent marks: unidecode.unidecode(word_data)
tokenizer: nltk.word_tokenize(word_data)
    BTW if markov chains are used, tokenize first since removing punctuation will cause empty strings, better for training 
-->

# Index
## Requirements:
- requests (optional for testing)

## Running index server
From the project root:
```
$ python index/gpp_index_server.py
Server started http://localhost:8080

```
Keyboard interrupt to stop server.

## Querying the index
To make requests, use HTTP GET requests. Valid queries return JSON, invalid or help queries return HTML.
### Help
http://host_name:server_port/help (e.g. http://localhost:8080/help) provides an html help page.

### Examples
Some examples of queries returning json are: 
- http://localhost:8080/full
- http://localhost:8080/subs?q=query
- http://localhost:8080/st?q=test

These results are basically a subset of the full index, allowing faster searching and flexible results, e.g. http://localhost:8080/st?q=query will return all words starting with 'query', allowing the online serving module to decide how to serve results.

An example on how to access this result:
```python
# Requests example (pip install requests)
import requests

r = requests.get('http://localhost:8080/st?q=query')
if r.status_code == 200:
    index = r.json()    # the json contents can be easily translated into a dict
    print(type(index))
    print(index)
    print()

    # Iterate through words (tokens)
    for token in list(index.keys()):
        print(token + ':')
        # Iterate through pages where the token appears
        for item in index[token]:
            print("    {}: {}".format(item['url'], item['count']))
```
Results:
```python
>>> import requests
>>> r = requests.get('http://localhost:8080/st?q=query')
>>> if r.status_code == 200:
...     index = r.json()    # the json contents can be easily translated into a dict
...     print(type(index))
...     print(index)
...     print()
...
<class 'dict'>
{'query': [{'url': 'www.querulousness.com', 'count': 49}, {'url': 'www.questers.com', 'count': 44}, {'url': 'www.quested.com', 'count': 44}, {'url': 'www.question.com', 'count': 43}, {'url': 'www.querying.com', 'count': 38}, {'url': 'www.querulously.com', 'count': 36}, {'url': 'www.quern.com', 'count': 34}, {'url': 'www.querulousnesses.com', 'count': 31}, {'url': 'www.questing.com', 'count': 30}, {'url': 'www.querists.com', 'count': 23}, {'url': 'www.quester.com', 'count': 21}, {'url': 'www.query.com', 'count': 7}, {'url': 'www.quest.com', 'count': 5}, {'url': 'www.querulous.com', 'count': 2}], 'querying': [{'url': 'www.questing.com', 'count': 49}, {'url': 'www.questionable.com', 'count': 41}, {'url': 'www.querulously.com', 'count': 38}, {'url': 'www.querulousnesses.com', 'count': 38}, {'url': 'www.querns.com', 'count': 35}, {'url': 'www.questers.com', 'count': 32}, {'url': 'www.quested.com', 'count': 31}, {'url': 'www.querulousness.com', 'count': 30}, {'url': 'www.quern.com', 'count': 29}, {'url': 'www.querying.com', 'count': 18}, {'url': 'www.quest.com', 'count': 8}, {'url': 'www.query.com', 'count': 5}, {'url': 'www.querulous.com', 'count': 3}]}

>>> for token in list(index.keys()):
...     print(token + ':')
...     # Iterate through pages where the token appears
...     for item in index[token]:
...         print("    {}: {}".format(item['url'], item['count']))
...
query:
    www.querulousness.com: 49
    www.questers.com: 44
    www.quested.com: 44
    www.question.com: 43
    www.querying.com: 38
    www.querulously.com: 36
    www.quern.com: 34
    www.querulousnesses.com: 31
    www.questing.com: 30
    www.querists.com: 23
    www.quester.com: 21
    www.query.com: 7
    www.quest.com: 5
    www.querulous.com: 2
querying:
    www.questing.com: 49
    www.questionable.com: 41
    www.querulously.com: 38
    www.querulousnesses.com: 38
    www.querns.com: 35
    www.questers.com: 32
    www.quested.com: 31
    www.querulousness.com: 30
    www.quern.com: 29
    www.querying.com: 18
    www.quest.com: 8
    www.query.com: 5
    www.querulous.com: 3
>>>

```

## Test data
Test indices exist in the test_indices/ directory, large (~113K words with <15 pages each) is used by default. Other sizes are medium (~66K words), small (~10K words), and tiny (100 words)