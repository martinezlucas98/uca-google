<!--
## TODO
- [ ] Unit tests
Indexes:
Page rank:
    Calculate ranking based on backlinks, counts, etc

## Notes
string punctuation: word_data.translate(word_data.maketrans('', '', string.punctuation + '…°'))
strip accent marks: unidecode.unidecode(word_data)
tokenizer: nltk.word_tokenize(word_data)
    BTW if markov chains are used, tokenize first since removing punctuation will cause empty strings, better for training 
-->

# Index
## Settings
Various settings for both running the indexer and the server are found in settings.py
## Building index
To run the indexer execute index.py. For usage/help use (from the project root)
```$ python index/index.py --help
```
When executing the indexer, every dot is a file scanned. If no dots appear and the program prints new lines, check if the location settings.scraped_files_dir points to the right place and files with the name "uc_*.json" exist.

## Running index server
From the project root (*settings.py contains hostname and port settings, change them as needed*):
```
$ python index/index_server.py
Server started http://localhost:8080
PID: 1234

```
Keyboard interrupt to stop server.

To run the server in the background:
```
$ nohup python index/index_server.py &
[1] 1234
nohup: ignoring input and appending output to 'nohup.out'
```
And to terminate:
```
$ kill 1234
```

## Querying the index
To make requests, use HTTP GET requests. Valid queries return JSON, invalid or help queries return HTML.
### Help
http://host_name:server_port/help (e.g. http://localhost:8080/help) provides an html help page.

### Examples
Some examples of queries returning json are: 
- http://localhost:8080/full
- http://localhost:8080/subs?q=query
- http://localhost:8080/st?q=test

These results are a subset of the full index, allowing faster searching and flexible results, e.g. http://localhost:8080/st?q=query will return all words starting with 'query', allowing the online serving module to decide how to serve results.

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

## Unittest
Launch the index server on localhost:8080 with a non-empty index to run unit tests. \
TODO: make test independent

## Test data
Test index contained in indices/index.pickle, and contains ~1100 tokens for 8 pages.