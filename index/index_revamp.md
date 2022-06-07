# Problems
1. Slow index serving response time
2. Underwhelming online serving ranking

# Causes
1. Big chunks of data transferred many times
2. Poor ranking algorithm, because too little page data is available

# Solution
A separate page database containing title, url, description (if available), and raw page text, and an ID for the key

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