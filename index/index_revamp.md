# Index Revamp
The index specifications described in the first Google Doc is not very good, so some changes were made to improve on them.

# Problems
1. Slow index serving response time
2. Underwhelming online serving ranking
3. Slow indexing process
4. Inflated file sizes

# Causes
1. Big chunks of data transferred many times
2. Poor ranking algorithm, because too little page data is available
3. A lot of disc I/O
4. Lots of redundant information stored

# Solution
A separate page database containing title, url, description, and raw page text, and an ID for the key.

Online Serving can then evaluate the text and the token referencing it in the index and make a more sensible page rank algorithm, and at the same time redundant page data will not be sent again.

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

### Revision

```python
tokens = {
    'token': {
        123: 1,
        ...
    }
}
```
Since the value to the key `'token'` was a list of dictionaries with only two values, the worst attributes of both structures was showing: no use for the iterability of lists, and no hash map for pages in a token.

The format was simplified, since there was only two values anyways, to a dictionary with page IDs as keys and counts as values.

## Index server

The server has undergone some optimizations as well. Indices are now loaded into memory, cutting down on file I/O further.

Since file transfer is now the bigger bottleneck, options were added for querying the index more specifically. When asking for several words, the index now returns pages with all the words in them, with the option to return any page with at least one of them.

Another option is to ignore page links in the return, since some ranking algorithms do not need them, which cuts down on response size.

The return type can also be specified as one of three types:
- json
- compressed with zlib deflate
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