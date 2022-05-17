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
    
    def add_entry(self, word: str, url: str, count: int):
        '''Adds a word's entry with the url of and appearance count in a page.'''
        
        if count <= 0:
            return
        
        # Add new word
        if word not in self.index:
            self.index[word] = [{'url': url, 'count': count}]
        # Or add to existing word
        else:
            # Check if the word has not been indexed on that page before (for updates)
            if len([page for page in self.index[word] if page['url'] == url]) == 0:
                self.index[word].append({'url': url, 'count': count})
            else:
                # If it has, just update the count. Shouldn't ever happen but just in case
                for page in self.index[word]:
                    if page['url'] == url:
                        page['count'] = count
                        break
        
    def del_entry(self, word: str, url: str):
        '''Removes an entry for a word using the url. Calls add_entry with count=0'''
        self.add_entry(word, url, 0)
    
    def del_word(self, word: str):
        '''Removes a word from the index, deleting all page entries for it.'''
        self.index.pop(word)
    
    def dump(self, filename: str = 'gpp_index.pickle'):
        '''Dumps the obj so it can be updated later.'''
        self.sort()
        with open(filename, 'wb') as file:
            pickle.dump(self, file)
    
    def dump_index(self, index_filename: str = 'index.pickle'):
        '''Dumps self.index into a pickled file. Sorts before dumping.
        
        Unpickling will result in a dict, not a GPP_Index object.'''
        self.sort()
        with open(index_filename, 'wb') as file:
            pickle.dump(self.index, file)

    def sort(self):
        '''Sort pages associated with words by count, and words themselves alphabetically'''
        for token, page in self.index.items():
            page.sort(key=page_count, reverse=True)
        # convert dict to list of (token, pages) tuples, sort (this will use token), and convert back to dict before returning
        self.index = dict(sorted(list(self.index.items())))
    
    def build_index(self, html_content: str, url: str):
        '''# WIP
        
        Goes through the return data of a scraped page, indexing the text.
        
        Assumed format: {'content': ["<tags>text</tags>"], 'links': ["link1", "link2", ...]}'''
        
        # TBD:
        # - Where are the scraped pages being stored?
        # - How do I find the url to a page? Currently there is page content and links only
        # - Do I bother with the Markov chain idea?
        
        # Check if the page has been indexed before, if so this is a job for update_index()
        content_hash = hashlib.md5(html_content.encode())
        if url in self.indexed_urls:
            if self.indexed_urls[url] != content_hash.hexdigest():
                self.update_index(html_content, url)
                self.indexed_urls[url] = content_hash.hexdigest()
            return
        # Add to list of urls
        self.indexed_urls[url] = content_hash.hexdigest()
        
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
        for token, count in counts.items():
            # Check that avoids tokens like ',' being indexed
            if len([symbol for symbol in token if symbol in string.punctuation]) > 0:
                self.add_entry(token, url, count)
        # No punctuation version, is that needed? NLTK separates most punctuation into its own tokens anyways, easy to filter

    def update_index(self, html_content: str, url: str):
        '''Handles updating a page's indexes, particularly deleting words that were removed/replaced.'''

        # TODO
        # Remove previous entries entirely
        # Read entries
        pass
    
if __name__ == '__main__':
    # Examples
    test_index = GPP_Index()
    test_index.index['word'] = [{'url':'test.com', 'count':42}]
    test_index.dump('test_index.pickle')