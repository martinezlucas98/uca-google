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
http://host_name:server_port/help (e.g. http://localhost:8080/help) provides an html help page. Other queries return json files.

## Test data
Test indices exist in the test_indices/ directory, large (~113K words with <15 pages each) is used by default. Other sizes are medium (~66K words), small (~10K words), and tiny (100 words)

<!--
## TODO
- [ ] Unit tests
Indexes:
- [ ] Multiple words (?)
-->