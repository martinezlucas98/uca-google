from datetime import datetime
import hashlib
import pickle
import string
from typing import Counter

import nltk
import unidecode
from bs4 import BeautifulSoup


def page_count(page):
    '''Auxiliary function for sorting pages in the index
    
    Usage: page.sort(key=page_count)'''
    return page['count']

class GPP_Index:
    '''Index object with an actual dictionary as the centerpiece and additional methods for building it.
    
    The dump() method will dup the 
    
    The dump_index() method will create a pickle file with the dictionary, the index itself, which will be used
    for searching and permanent storage of the index.'''
    
    def __init__(self, pickled_gpp_index: str = None):
        self.index = dict()
        self.indexed_urls = dict() # format = {'https://example.com': 'hash'}
        
        # Load from pickled file
        if pickled_gpp_index is not None:
            with open(pickled_gpp_index, 'rb') as file:
                instance = pickle.load(file)
            for attr, value in instance.__dict__.items():
                self.__dict__[attr] = value
    
    def add_entry(self, word: str, url: str, count: int, date: datetime, links: list, title: str, description: str):
        '''Adds a word's entry with the url of and appearance count in a page.'''
        
        if count <= 0:
            return
        
        # Add new word
        if word not in self.index:
            self.index[word] = [{'url': url, 'count': count, 'date': date, 'title': title, 'description': description}]
        # Or add to existing word
        else:
            # Updates will involve deleting entries, so repeated entries should not happen
            self.index[word].append({'url': url, 'count': count, 'date': date, 'title': title, 'description': description})
        
    def del_page(self, url: str):
        '''Removes all entries associated with a url.'''
        for token, page in [(token, page) for token in self.index for page in self.index[token] if page['url'] == url]:
            self.index[token].remove(page)
    
    def dump(self, filename: str = 'gpp_index.pickle'):
        '''Dumps the obj so it can be updated later.'''
        self.strip()
        self.sort()
        with open(filename, 'wb') as file:
            pickle.dump(self, file)
    
    def dump_index(self, index_filename: str = 'index.pickle'):
        '''Dumps self.index into a pickled file. Sorts before dumping.
        
        Unpickling will result in a dict, not a GPP_Index object.'''
        self.strip()
        self.sort()
        with open(index_filename, 'wb') as file:
            pickle.dump(self.index, file)

    def sort(self):
        '''Sort pages associated with words by count, and words themselves alphabetically.'''
        for token, page in self.index.items():
            page.sort(key=page_count, reverse=True)
        # convert dict to list of (token, pages) tuples, sort (this will use token), and convert back to dict before returning
        self.index = dict(sorted(list(self.index.items())))
    
    def strip(self):
        '''Removes words without entries.'''
        for token in [token for token in self.index if self.index[token] == []]:
            self.index.pop(token)
    
    def build_index(self, html_content: str, url: str, date: datetime, links: list):
        '''# WIP
        
        Goes through the return data of a scraped page, indexing the text.
        
        Assumed format: {'content': ["<tags>text</tags>"], 'links': ["link1", "link2", ...]}'''
        
        # TBD:
        # - Where are the scraped pages being stored?
        # - How do I find the url to a page? Currently there is page content and links only
        # - Do I bother with the Markov chain idea?
        
        # Check if the page has been indexed before, if so this is a job for update_index()
        content_hash = hashlib.md5(html_content.encode())
        is_update = False
        if url in self.indexed_urls:
            if self.indexed_urls[url] != content_hash.hexdigest():
                is_update = True
            else:
                return # as this page is up to date on the index
        
        # Start by adding in BeautifulSoup for html parsing
        content = BeautifulSoup(html_content, 'html.parser')
        
        page_text = content.text.strip()
        # normalize accents and remove weird symbols
        page_text = page_text.translate('', '', page_text.maketrans('°')) # add more if necessary
        page_text = unidecode.unidecode(page_text)
        # remove punctuation
        # no_punct_page_text = page_text.translate(page_text.maketrans('', '', string.punctuation))

        # Tokenize
        tokens = nltk.word_tokenize(page_text)
        # no_punct_tokens = nltk.word_tokenize(no_punct_page_text)
        
        # Count tokens
        counts = dict(Counter(tokens))
        # no_punct_counts = dict(Counter(no_punct_tokens))
        
        # Index
        if is_update:
            self.update_index(html_content, url, date, links)
            return
        
        for token, count in counts.items():
            # Check that avoids tokens like ',' being indexed
            if len([symbol for symbol in token if symbol not in string.punctuation]) > 0:
                self.add_entry(token, url, count, date, links)
        # No punctuation version, is that needed? NLTK separates most punctuation into its own tokens anyways, easy to filter

        # Done, add to list of urls
        self.indexed_urls[url] = content_hash.hexdigest()

    def update_index(self, html_content: str, url: str, date: datetime, links: list):
        '''Handles updating a page's indexes, particularly deleting words that were removed/replaced.'''

        # TODO
        # Remove previous entries entirely
        # Read entries
        pass
    
        # Done, add to list of urls
        content_hash = hashlib.md5(html_content.encode())
        self.indexed_urls[url] = content_hash.hexdigest()
    
if __name__ == '__main__':
    # Examples
    test_index = GPP_Index()
    test_index.add_entry('word', 'example.com', 15, datetime(2022, 5, 17), [], 'Title', 'Description text')
    test_index.add_entry('example', 'example.com', 11, datetime(2022, 5, 17), [], 'Title', 'Description text')
    test_index.add_entry('word', 'example.org', 17, datetime(2022, 5, 17), [], 'Title 2', 'Description text 2')
    print(test_index.index)
    test_index.del_page('example.com')
    print('\n', test_index.index)