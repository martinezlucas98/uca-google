# Index Revamp
The index specifications described in the first Google Doc are not very good, so some changes were made to improve on them.

# Problems
1. Slow index server response time
2. Underwhelming online serving ranking
3. Slow indexing process
4. Inflated file sizes

# Causes
1. Big chunks of data transferred many times
2. Poor ranking algorithm, because too little page data is available
3. A lot of disc I/O
4. Lots of redundant information stored

# Solutions
A separate page database containing title, url, description, and raw page text, and an ID for the key. \
Online Serving can then evaluate the text and the token referencing it in the index and make a more sensible page rank algorithm, and at the same time redundant page data will not be sent again. (This solves problems 1. and 2. (in part) and 4.)

A more impactful solution for problem 1. is keeping index files in memory. If the file sizes are to be made smaller, this is the option that makes the most sense, and cuts down on file I/O. The return format can also be changed: before, the server only worked with json, but it could also return serialized or compressed data just as well.

For the indexing process, problem 3., which is offline but still too slow to be viable, saving data repeatedly was the culprit. Instead of saving the index after every page added, the indexer will only save once in a while, a parameter the user can set. This means a lot of pages can be processed before having to save. \
Another option is to use an append-only data structure, so only the changes need to be written to disc and not the entire index, but this was not implemented.

## Specifications

### Old index

```python
idx = {
    'token': [
        {
            'url': 'www.a.com',
            'count': 1,
            'date': 1654180874.7023404,
            'title': 'Title line',
            'description': 'most likely None',
            'links': ['list', 'of', 'links', 'on', 'page']
        }
    ],
    ...
}
```

This format could send repeat data if the same page featured different (or similar) searched words. E.g. 'catolica' and 'catolicas' both appear on similar pages and both result from searching the index for 'catol'.

Add to this the fact that some pages have link lists that have >1000 items, meaning repeated and long data is sent. This is slow, since it is converted to utf-8 from a data structure and back.

### New index
```python
tokens = {
    'token': [
        {
            'id': 123,
            'count': 1
        },
        ...
    ],
    ...
}

pages = {
    123: {
        'url': 'www.a.com',
        'date': 1654180874.7023404,
        'title': 'Title line',
        'description': 'meta tag description if available, else None',
        'links': ['list', 'of', 'page', 'links'],
        'content': 'Full page text contents, stripped of HTML and condensed into a string for ranking and description searching'
    },
    ...
}
```
The new index is condensed and avoids sending repeat data. Having only an id to associate to a page makes the data transferred exponentially smaller, and avoids sending data repeatedly by only sending the id of a page.

Pages are stored separately to the index and can be accessed separately. They include the text in the page for the serving algorithm to be able to form a small description of the page.

Although this format is already very good, one obvious change came in a later revision.

### Revision

```python
tokens = {
    'token': {
        123: 1,
        ...
    }
}
```
Since the value to the key `'token'` was a list of dictionaries with only two values, the data stored could not be accessed via the id.

The format was simplified, since there was only two values anyways, to a dictionary with page IDs as keys and counts as values. In the unlikely case a list was the preferred structure, one could be made with dictionary methods .keys() or .items().

## Index server

The server has undergone some optimizations as well. Indices are now loaded into memory, cutting down on file I/O further.

Since file transfer is now the bigger bottleneck, options were added for querying the index more specifically. When asking for several words, the index now returns pages with all the words in them, with the option to return any page with at least one of them.

Another option is to ignore page links in the return, since some ranking algorithms do not need them, which cuts down on response size.

The return type can also be specified as one of three types:
- json
- json compressed with zlib deflate
- serialized with pickle

The `response_filetype_test.py` scripts executes three identical queries with different response types. Results:
- Serialized:
    1st speed
    2nd space
- Json:
    2nd speed (2x serialized)
    3rd space (barely more than serialized)
- Compressed:
    3rd speed (4.7x serialized)
    1st space (1/3x serialized)

So for speed, pickled return is better, and for debugging, json is better. Compression, at least this implementation, is not worth it.