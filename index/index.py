import glob
import hashlib
import json
import os
import pickle
import re
import signal
import string
import time
from sys import argv
from time import sleep
from typing import Counter

import nltk
import unidecode
from bs4 import BeautifulSoup

import settings

class GPP_Index:
    '''Index object with an actual dictionary as the centerpiece and additional methods for building it.
    
    The dump() method will dup the 
    
    The dump_index() method will create a pickle file with the dictionary, the index itself, which will be used
    for searching and permanent storage of the index.'''
    
    def __init__(self, pickled_gpp_index: str = None):
        self.index = dict()
        self.indexed_urls = dict() # format = {'https://example.com': 'hash'}
        # for more space efficient index serving
        self.pages = dict()
        self.url_to_id = dict() # format = {'https://example.com': id}
        
        # Load from pickled file
        if pickled_gpp_index is not None:
            try:
                with open(pickled_gpp_index, 'rb') as file:
                    instance = pickle.load(file)
                for attr, value in instance.__dict__.items():
                    self.__dict__[attr] = value
            except FileNotFoundError:
                pass # Only try to load if the file exists
    
    def add_entry(self, token: str, page_id: int, count: int):
        '''Adds a word's (token) entry with the url of and appearance count in a page.'''
        
        if count <= 0:
            return
        
        # entry = {'url': url, 'count': count, 'date': timestamp, 'title': title, 'description': description, 'links': links}
        # Add new token
        if token not in self.index:
            self.index[token] = {}
        # And add page_id to token
        # Updates will involve deleting entries, so repeated entries should not happen
        self.index[token][page_id] = count
        
    def del_page(self, url: str):
        '''Removes all entries associated with a url. May leave empty tokens on the index, call strip() to remove them'''
        try:
            page_id = self.url_to_id[url]
            for token, page in [(token, page) for token in self.index for page in self.index[token] if page == page_id]:
                self.index[token].pop(page)
            
            self.pages.pop(page_id)
        except KeyError:
            return
    
    def del_page(self, page_id: int):
        '''Removes all entries associated with a page. May leave empty tokens on the index, call strip() to remove them'''
        try:
            for token, page in [(token, page) for token in self.index for page in self.index[token] if page == page_id]:
                self.index[token].pop(page)
            
            self.pages.pop(page_id)
        except KeyError:
            return
    
    def dump(self, filename: str = settings.dev_index_obj, self_only = False):
        '''Dumps self so it can be updated later.'''
        self.strip()
        # self.sort()
        try:
            with open(filename, 'wb') as file:
                pickle.dump(self, file)
        except FileNotFoundError:
            os.mkdir("index/indices")
            self.dump(filename)
            return
        if not self_only:
            self.dump_index(no_clean=True)
    
    def dump_index(self, index_filename: str = settings.index_filename, pages_filename: str = settings.indexed_pages_filename, no_clean: bool = False):
        '''Dumps self.index into a pickled file. Sorts before dumping.
        
        Unpickling will result in a dict, not a GPP_Index object.'''
        if not no_clean:
            self.strip()
            # self.sort()
        with open(index_filename, 'wb') as file:
            pickle.dump(self.index, file)
        with open(pages_filename, 'wb') as file:
            pickle.dump(self.pages, file)
    
    def strip(self):
        '''Removes words without entries.'''
        for token in [token for token in self.index if self.index[token] == []]:
            self.index.pop(token)
    
    def build_index(self, html_content: str, url: str, timestamp: float, links: list, forced: bool = False):
        '''Goes through the return data of a scraped page, indexing the text. Returns a string if the page was indexed'''
        
        # Check if the page has been indexed before, if so delete the page off the index as if it was never indexed
        content_hash = hashlib.md5(html_content.encode())
        is_update = False
        if url in self.indexed_urls:
            if self.indexed_urls[url] != content_hash.hexdigest() or forced:
                self.del_page(url) # delete and re-index as anything could have changed
                is_update = True
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
            description = description['content'][:settings.description_len]
        # No UC pages have a meta description tag, but the feature is there just in case one eventually does
        # Else, take the first bit of the body text
        else:
            try:
                description = soup.body.find('p').text.strip()[:settings.description_len]
                if len(description) == 0:
                    description.erroneous
            except AttributeError:
                description = soup.get_text(' ', strip=True)[:settings.description_len]
        
        try:
            page_text = soup.get_text(' ', strip=True)
            # normalize accents and remove weird symbols
            page_text = page_text.translate(page_text.maketrans('°/', '  ')) # add more if necessary
            page_text = unidecode.unidecode(page_text)
            rex = re.compile(r'\W+')
            page_text = rex.sub(' ', page_text).lower()
        except:
            page_text = None
        
        # Store page information
        try:
            page_id = max(self.pages) + 1
        except ValueError:
            page_id = 1
        self.pages[page_id] = {
            'url': url,
            'date': timestamp,
            'title': title,
            'description': description,
            # links like '/wp...' or '#' get ignored
            'links': [link for link in links if link.startswith('http')],
            # This content item contains a lot of text, used for scoring pages.
            # The computation is done at run time in online serving, but it could
            # be done at index time
            'content': page_text
        }
        self.url_to_id[url] = page_id
        
        # No body, no words to index. The head alone is not interesting enough
        if page_text is not None:
            # Tokenize
            try:
                tokens = [token for token in nltk.word_tokenize(page_text, language='spanish')]
            except LookupError:
                nltk.download('punkt')
                tokens = [token for token in nltk.word_tokenize(page_text, language='spanish')]
            
            # Count tokens
            counts = dict(Counter(tokens))
            
            # Index
            for token, count in counts.items():
                # Check that avoids tokens like ',' being indexed
                if len([symbol for symbol in token if symbol not in string.punctuation]) > 0:
                    self.add_entry(token, page_id, count)
            # No punctuation version, is that needed? NLTK separates most punctuation into its own tokens anyways, easy to filter

        # Done, add to list of urls
        self.indexed_urls[url] = content_hash.hexdigest()
        
        # Message
        if forced:
            return f"{url} indexed (forced)"
        elif is_update:
            return f"{url} re-indexed (updated)"
        return f"{url} indexed (first time)"

def run_indexer(run_forever: bool = False, interval: float = 0, silent: bool = False, verbose: bool = False, force: bool = False, test_dir: str = None):
    '''Handles indexing frequency and file handling for the index.
    
    Every time a file is indexed, the index is saved so interrupt signals do not corrupt it.
    To stop if running forever use 'Ctrl+C' or send a SIGTERM using 'kill <PID>'
    
    force = True will cause all already indexed files to be re-indexed unconditionally once.'''
    
    # this only exists for testing
    if test_dir is None:
        scraped_files_dir = settings.scraped_files_dir
        dev_index_obj = settings.dev_index_obj
        index_filename = settings.index_filename
        indexed_pages = settings.indexed_pages_filename
    else:
        scraped_files_dir = test_dir + '/'
        dev_index_obj = test_dir + '/' + 'test_dev_index.pickle'
        index_filename = test_dir + '/' + 'test_index.pickle'
        indexed_pages = test_dir + '/' + 'indexed_pages.pickle'
    
    index = GPP_Index(dev_index_obj)

    # Saves index to disc safely, not overwriting until the file is complete in case the process dies
    # to avoid corrupting the indices
    # Could be improved with https://github.com/google/leveldb
    def save_index(msg):
        if msg is not None and msg != '':
            index.dump(dev_index_obj + '~', self_only=True)
            os.rename(dev_index_obj + '~', dev_index_obj)
            index.dump_index(index_filename + '~', indexed_pages + '~')
            os.rename(index_filename + '~', index_filename)
            os.rename(indexed_pages + '~', indexed_pages)
            if not silent:
                if verbose: print('\nSaved index with new pages\n' + msg)
                else: print("\nSaved index")
    
    # Optimization: saving once every interval
    ts = time.time()
    msg = ''

    # Index will save after each file processed
    # This process needs to be safe, so in case a SIGTERM is received the index is not corrupted
    try:
        if test_dir is None:
            print("Indexer running, Ctrl+C to interrupt")
            print(f"Scanning {scraped_files_dir}, saving index every {interval} seconds")
        while True: # I want a DO WHILE style of loop, i.e. run at least once
        # DO
            # scan files in scraped_files_dir
            scrape_list = glob.glob(scraped_files_dir + "uc_*.json")
            for filename in scrape_list:
                if not silent: print('.', end='', flush=True)
                with open(filename) as file:
                    page = json.load(file)
                
                # Index current page
                fetch_ts = os.stat(filename).st_mtime
                # Sometimes there are no links
                try:
                    links = [link['url'] for link in page['url_links']]
                except:
                    links = []
                
                msg_ = index.build_index(page['url_html'][0], page['url_self'][0], fetch_ts, links, force)
                if msg_ is not None:
                    msg += msg_
                msg += '\n'

                # Optimization: saving once every interval
                if time.time() - ts >= interval:
                    # Save index object and index
                    # Any deletions or additions to the index were made in memory, receiving a SIGTERM before this would
                    # not have damaged the index on disk
                    save_index(msg)
                    msg = ''
                    ts = time.time()
            
        # WHILE
            # In case scan finished before interval end
            save_index(msg)
            msg = ''
            
            # Stats
            if not silent:
                print(f"\nStats:\n\t{len(index.pages)} pages\n\t{len(index.index)} words\n")
                # print()
            if not run_forever:
                break
            force = False
    # Handle sigterm
    except KeyboardInterrupt:
        stop_indexer()

# For handling signals while running forever
def stop_indexer():
    print("Indexer stopped")
    exit(0)

if __name__ == '__main__':
    
    # Handle args
    forever = False
    interval = 5
    silent = False
    verbose = False
    force = False
    usage_msg = f"Usage: {argv[0]} [--forever] [-t <interval>] [-s] [-v] [--force] [-h | --help]"
    if '--forever' in argv:
        forever = True
    if '-t' in argv:
        try:
            interval = int(argv[argv.index('-t') + 1])
            if interval <= 0:
                raise "Invalid"
        except:
            print(usage_msg)
            exit(1)
    if '-s' in argv:
        silent = True
    elif '-v' in argv:
        verbose = True
    if '-h' in argv or '--help' in argv:
        print(usage_msg + '\n')
        help_strings = [
            "   --forever       Runs in a loop, to interrupt use keyboard interrupt (Ctrl+C).",
            "   --force         Indexes or re-indexes every file, even if it was not changed and can be skipped.",
            "   -s              Silent mode, no logging. Incompatible with -v and takes priority.",
            "   -v              Verbose logging. Ignored when -s is used.",
            "   -h  --help      Show this menu and terminate.",
            "   -t <interval>   Save index at least once every interval of seconds. Default value is 5."
        ]
        help_strings.sort()
        for line in help_strings:
            print(line)
        exit(0)
    if '--force' in argv:
        force = True

    # Handle sigterm
    signal.signal(signal.SIGTERM, stop_indexer)
    
    run_indexer(forever, interval, silent, verbose, force)
    exit(0)
