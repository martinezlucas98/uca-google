import json
import os
import pickle
import string
import time
import unittest

from index import run_indexer
from index import GPP_Index


class IndexTest(unittest.TestCase):
    def setUp(self):
        # for tmp filenames
        self.time = time.time()
    
    def test_add_entry(self):
        gppi = GPP_Index()
        gppi.add_entry('test', 123, 456)
        self.assertEqual(gppi.index['test'][123], 456)
    
    def test_del_page(self):
        gppi = GPP_Index()
        gppi.add_entry('test', 1, 1)
        gppi.add_entry('tests', 1, 2)
        gppi.add_entry('tester', 2, 1)
        gppi.del_page(1)
        self.assertEqual(len([word for word in gppi.index if len(gppi.index[word]) != 0]), 1)
    
    def test_dump_index(self):
        gppi = GPP_Index()
        gppi.add_entry('test', 123, 456)
        tmp_fn = '.' + str(self.time) + '.tmp'
        gppi.dump_index(tmp_fn)
        with open(tmp_fn, 'rb') as file:
            i = pickle.load(file)
        os.remove(tmp_fn)
        self.assertEqual(gppi.index, i)
    
    def test_dump_object(self):
        gppi = GPP_Index()
        gppi.add_entry('test', 123, 456)
        tmp_fn = '.' + str(self.time) + '.tmp'
        gppi.dump(tmp_fn, True)
        gppi_dupe = GPP_Index(tmp_fn)
        os.remove(tmp_fn)
        self.assertEqual(gppi.index, gppi_dupe.index)
    
    def test_strip(self):
        gppi = GPP_Index()
        gppi.add_entry('test', 123, 456)
        gppi.index['tester'] = []
        gppi.strip()
        self.assertEqual(len(gppi.index), 1)
    
    def test_build_index(self):
        gppi = GPP_Index()
        gppi.build_index("<html><head><title>Title!</head></title><body><p>Long text about something, with added punctuation... is it good-enough?<br>'¡And äccént märks!'</p></body></html>",
                         'http://www.text.com', self.time, [], True)
        self.assertGreater(len(gppi.index), 0)

    def test_normalization(self):
        gppi = GPP_Index()
        gppi.build_index("<html><head><title>Title!</head></title><body><p>Long text about something, with added punctuation... is it good-enough?<br>'¡And äccént märks!'</p></body></html>",
                         'http://www.text.com', self.time, [])
        # revisa si palabras terminan en '-' o tienen acentos
        self.assertEqual(len([token for token in gppi.index if token[0] in string.punctuation or token[-1] in string.punctuation]) + len([token for token in gppi.index for char in token if char not in string.printable]), 0)
    
    def test_build_index_update_ignore(self):
        gppi = GPP_Index()
        gppi.build_index("<html><head><title>Title!</head></title><body><p>Long text about something, with added punctuation... is it good-enough?<br>'¡And äccént märks!'</p></body></html>",
                         'http://www.text.com', self.time, [])
        msg = gppi.build_index("<html><head><title>Title!</head></title><body><p>Long text about something, with added punctuation... is it good-enough?<br>'¡And äccént märks!'</p></body></html>",
                         'http://www.text.com', self.time, [])
        self.assertEqual(msg, None)

    def test_build_index_update_reindex(self):
        gppi = GPP_Index()
        gppi.build_index("<html><head><title>Title!</head></title><body><p>Long text about something, with added punctuation... is it good-enough?<br>'¡And äccént märks!'</p></body></html>",
                         'http://www.text.com', self.time, [])
        msg = gppi.build_index("<html><head><title>Title changed!</head></title><body><p>Long text about something, with added punctuation... is it good-enough?<br>'¡And äccént märks!'</p></body></html>",
                         'http://www.text.com', self.time, [])
        self.assertNotEqual(msg, None)

    def test_build_index_force_reindex(self):
        gppi = GPP_Index()
        gppi.build_index("<html><head><title>Title!</head></title><body><p>Long text about something, with added punctuation... is it good-enough?<br>'¡And äccént märks!'</p></body></html>",
                         'http://www.text.com', self.time, [])
        msg = gppi.build_index("<html><head><title>Title!</head></title><body><p>Long text about something, with added punctuation... is it good-enough?<br>'¡And äccént märks!'</p></body></html>",
                         'http://www.text.com', self.time, [], True)
        self.assertNotEqual(msg, None)

    def test_run_indexer(self):
        tmp_dn = '.' + str(self.time)
        tmp_fn = 'uc_' + str(self.time) + '.json'
        os.mkdir(tmp_dn)
        content = {
            "url_self": ["http://www.text.com"],
            "url_html": ["<html><head><title>Title!</head></title><body><p>Long text about something, with added punctuation... is it good-enough?<br>'¡And äccént märks!'</p></body></html>"],
            "url_links": []
            }
        with open(tmp_dn + '/' + tmp_fn, 'w') as file:
            json.dump(content, file)
        
        run_indexer(test_dir=tmp_dn, silent=True)
        
        gppi = GPP_Index(tmp_dn + '/test_dev_index.pickle')
        os.remove(tmp_dn + '/' + tmp_fn)
        os.remove(tmp_dn + '/test_dev_index.pickle')
        os.remove(tmp_dn + '/test_index.pickle')
        os.remove(tmp_dn + '/indexed_pages.pickle')
        os.removedirs(tmp_dn)
        
        self.assertGreater(len(gppi.index), 0)

if __name__ == '__main__':
    unittest.main()
