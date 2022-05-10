# Index
## Requirements:
- requests (optional for testing)

## Running index server
From the project root:
```bash
$ python index/gpp_index_server.py
Server started http://localhost:8080

```
Keyboard interrupt to stop server.

## Querying the index
http://host_name:server_port/help (e.g. http://localhost:8080/help) provides an html help page.\
Other queries return json files.

Some examples of queries returning json are: 
- http://localhost:8080/full
- http://localhost:8080/subs?q=query
- http://localhost:8080/st?q=teste

These results are basically a subset of the full index, allowing faster searching and flexible results, e.g. http://localhost:8080/st?q=teste will return all words starting with 'teste', allowing the online serving module to decide how to serve results.

An example on how to access this result:
```python
# Requests example (pip install requests)
import requests

r = requests.get('http://localhost:8080/st?q=teste')
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

## Test data
Test indices exist in the test_indices/ directory, large (~113K words with <15 pages each) is used by default. Other sizes are medium (~66K words), small (~10K words), and tiny (100 words)

<!--
## TODO
- [ ] Unit tests
Indexes:
- [ ] Multiple words (?)
-->