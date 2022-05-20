import glob
import hashlib
import json
import os
import pickle
import signal
import string
from typing import Counter

import nltk
import unidecode
from bs4 import BeautifulSoup

import settings


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
            try:
                with open(pickled_gpp_index, 'rb') as file:
                    instance = pickle.load(file)
                for attr, value in instance.__dict__.items():
                    self.__dict__[attr] = value
            except FileNotFoundError:
                pass # Only try to load if the file exists
    
    def add_entry(self, token: str, url: str, count: int, timestamp: float, links: list, title: str, description: str):
        '''Adds a word's (token) entry with the url of and appearance count in a page.'''
        
        if count <= 0:
            return
        
        entry = {'url': url, 'count': count, 'date': timestamp, 'title': title, 'description': description, 'links': links}
        # Add new token
        if token not in self.index:
            self.index[token] = [entry]
        # Or add to existing token
        else:
            # Updates will involve deleting entries, so repeated entries should not happen
            self.index[token].append(entry)
        
    def del_page(self, url: str):
        '''Removes all entries associated with a url. May leave empty tokens on the index, call strip() to remove them'''
        for token, page in [(token, page) for token in self.index for page in self.index[token] if page['url'] == url]:
            self.index[token].remove(page)
    
    def dump(self, filename: str = settings.dev_index_obj):
        '''Dumps self so it can be updated later.'''
        self.strip()
        self.sort()
        with open(filename, 'wb') as file:
            pickle.dump(self, file)
        self.dump_index(no_clean=True)
    
    def dump_index(self, index_filename: str = settings.index_filename, no_clean: bool = False):
        '''Dumps self.index into a pickled file. Sorts before dumping.
        
        Unpickling will result in a dict, not a GPP_Index object.'''
        if not no_clean:
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
    
    def build_index(self, html_content: str, url: str, timestamp: float, links: list):
        '''# WIP
        
        Goes through the return data of a scraped page, indexing the text.
        
        Assumed format: {'content': ["<tags>text</tags>"], 'links': ["link1", "link2", ...]}'''
        
        # TBD:
        # - Where are the scraped pages being stored?
        # - How do I find the url to a page? Currently there is page content and links only
        # - Do I bother with the Markov chain idea?
        
        # Check if the page has been indexed before, if so delete the page off the index as if it was never indexed
        content_hash = hashlib.md5(html_content.encode())
        if url in self.indexed_urls:
            if self.indexed_urls[url] != content_hash.hexdigest():
                self.del_page(url) # delete and re-index as anything could have changed
            else:
                return # as this page is up to date on the index
        
        # Start by adding in BeautifulSoup for html parsing
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Get title and description, both may be None
        title = soup.find('title')
        if soup.title is not None:
            title = soup.title.text.strip()

        description = soup.find('meta', {'name':'description'})
        if description is None:
            description = soup.find('meta', {'name':'Description'})
        if description is not None:
            description = description['content']
        
        
        # No body, no words to index. The head alone is not interesting enough
        if soup.body is not None:
            body_text = soup.body.get_text(' ').strip()
            # normalize accents and remove weird symbols
            body_text = body_text.translate(body_text.maketrans('', '', '°')) # add more if necessary
            body_text = unidecode.unidecode(body_text)

            # Tokenize
            try:
                tokens = [token.lower() for token in nltk.word_tokenize(body_text)]
            except LookupError:
                nltk.download('punkt')
                tokens = [token.lower() for token in nltk.word_tokenize(body_text)]
            
            # Count tokens
            counts = dict(Counter(tokens))
            
            # Index
            for token, count in counts.items():
                # Check that avoids tokens like ',' being indexed
                if len([symbol for symbol in token if symbol not in string.punctuation]) > 0:
                                                            # this means links like '//wp...' or '#' get ignored
                    self.add_entry(token, url, count, timestamp, [link for link in links if link.startswith('http')], title, description)
            # No punctuation version, is that needed? NLTK separates most punctuation into its own tokens anyways, easy to filter

        # Done, add to list of urls
        self.indexed_urls[url] = content_hash.hexdigest()

def run_indexer(run_forever: bool = False):
    '''Handles indexing frequency and file handling for the index.
    
    Every time a file is indexed, the index is saved so interrupt signals do not corrupt it.
    
    To stop if running forever use 'Ctrl+C' or send a SIGTERM using 'kill <PID>' '''
    
    index = GPP_Index(settings.dev_index_obj)
    
    # For handling signals while running forever
    def stop_indexer():
        print("Indexer stopped")
        exit(0)
    signal.signal(signal.SIGTERM, stop_indexer)
    
    
    # Index will save after each file processed
    # This process needs to be safe, so in case a SIGTERM is received the index is not corrupted
    try:
        while True: # I want a DO WHILE style of loop, i.e. run at least once
        # DO
            # scan files in settings.scraped_files_dir
            scrape_list = glob.glob(settings.scraped_files_dir + "uc_*.json")
            for filename in scrape_list:
                print(filename)
                with open(filename) as file:
                    page = json.load(file)
                
                # Index current page
                fetch_ts = os.stat(filename).st_mtime
                index.build_index(page['url_html'][0], page['url_self'][0], fetch_ts, [link['url'] for link in page['url_links']])

                # Save index object and index
                # Any deletions or additions to the index were made in memory, receiving a SIGTERM before this would
                # not have damaged the index on disk
                index.dump()
            
        # WHILE
            if not run_forever:
                break
    except KeyboardInterrupt:
        stop_indexer()

if __name__ == '__main__':
    run_indexer(False)
    exit(0)