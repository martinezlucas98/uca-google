import pickle

def page_count(page):
    '''Auxiliary function for sorting pages in the index
    
    Usage: page.sort(key=page_count)'''
    return page['count']

class GPP_Index:
    '''Index object with an actual dictionary as the centerpiece and additional methods for building it.
    
    The dump() method will create a pickle file with the dictionary, the index itself, which will be used
    for searching and permanent storage of the index.'''
    
    def __init__(self, pickled_file: str = None):
        if pickled_file is None:
            self.index = dict()
        else:
            with open(pickled_file, 'rb') as file:
                self.index = pickle.load(file)
    
    def add_entry(self, word: str, url: str, count: int):
        '''Adds or updates a word's entry with the new url and count.
        
        If the count is <= 0, the entry is removed.'''
        if word in self.index:
            if len([page for page in self.index[word] if page['url'] == url]) == 0:
                if count > 0:
                    self.index[word].append({'url': url, 'count': count})
                else:
                    for page in self.index[word]:
                        if page['url'] == url:
                            self.index[word].remove(page)
                            break
            else:
                for page in self.index[word]:
                    if page['url'] == url:
                        if count > 0:
                            page['count'] = count
                        else:
                            self.index[word].remove(page)
                        break
        elif count > 0:
            self.index[word] = [{'url': url, 'count': count}]
    
    def del_entry(self, word: str, url: str):
        '''Removes an entry for a word using the url. Calls add_entry with count=0'''
        self.add_entry(word, url, 0)
    
    def del_word(self, word: str):
        '''Removes a word from the index, deleting all page entries for it.'''
        self.index.pop(word)
    
    def dump(self, filename: str = 'index.pickle'):
        '''Dumps self.index into a pickled file. Sorts before dumping.
        
        Unpickling will result in a dict, not an Index object.'''
        self.sort()
        with open(filename, 'wb') as file:
            pickle.dump(self.index, file)

    def sort(self):
        '''Sort pages associated with words by count, and words themselves alphabetically'''
        for token, page in self.index.items():
            page.sort(key=page_count, reverse=True)
        # convert dict to list of (token, pages) tuples, sort (this will use token), and convert back to dict before returning
        self.index = dict(sorted(list(self.index.items())))

if __name__ == '__main__':
    # Examples
    idx = GPP_Index()
    idx.add_entry('test', 'www.test.org', 5)
    idx.add_entry('test', 'www.test.com', 12)
    idx.add_entry('tester', 'www.test.com', 1)
    idx.add_entry('test', 'www.test.com', 21)
    idx.add_entry('tests', 'www.test.com', 13)
    print(idx.index)
    idx.del_entry('tester', 'www.test.com')
    print(idx.index)
    idx.del_word('tester')
    print(idx.index)
    idx.dump()