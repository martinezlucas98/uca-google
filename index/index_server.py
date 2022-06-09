import json
import os
import pickle
import sys
import zlib
from http.server import BaseHTTPRequestHandler, HTTPServer
from signal import SIGTERM, signal

import settings


class IndexServer(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args):
        global quiet
        if not quiet:
            return super().log_message(format, *args)
    
    def send_json(self, object):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes('%s' % json.dumps(object), "utf-8"))
    
    def send_compressed_json(self, object):
        self.send_response(200)
        self.send_header("Content-type", "application/blob")
        self.end_headers()
        self.wfile.write(zlib.compress(bytes(json.dumps(object), "utf-8"), 3))
    
    def send_binary(self, object):
        self.send_response(200)
        self.send_header("Content-type", "application/blob")
        self.end_headers()
        self.wfile.write(pickle.dumps(object))
    
    def do_GET(self):
        pathstring, nil, paramstring = self.path.rstrip("/").partition('?')
        
        if pathstring == '/full':
            self.do_GET_index()
            return
        elif pathstring == '/subs':
            self.do_GET_index_search_by_substr(paramstring)
            return
        elif pathstring == '/i':
            self.do_GET_index_search_by_initials(paramstring)
            return
        elif pathstring == '/st':
            self.do_GET_index_search_by_stsubstr(paramstring)
            return
        elif pathstring == '/stc':
            self.do_GET_index_search_by_stsubstr(paramstring, send_type='deflate')
            return
        elif pathstring == '/sts':
            self.do_GET_index_search_by_stsubstr(paramstring, send_type='pickle')
            return
        elif pathstring == '/lit':
            self.do_GET_index_search_by_literal(paramstring)
            return
        elif pathstring == '/litc':
            self.do_GET_index_search_by_literal(paramstring, send_type='deflate')
            return
        elif pathstring == '/lits':
            self.do_GET_index_search_by_literal(paramstring, send_type='pickle')
            return
        elif pathstring == '/help':
            self.do_GET_help()
            return
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Top text</title></head>", "utf-8"))
        self.wfile.write(bytes("<p style=\"color:#c5c8c6\">Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body style=\"background-color:#1d1f21\">", "utf-8"))
        self.wfile.write(bytes("<p style=\"color:#c5c8c6\">This request returns nothing. <a href=\"http://{}:{}/help\">Help</a></p>".format(settings.host_name, settings.server_port), "utf-8"))
        self.wfile.write(bytes("<p style=\"color:#c5c8c6\">Bottom text</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
    
    def do_GET_index(self):
        '''Inefficient!
        Returns whole index as json.'''
        # with open(settings.index_filename, 'rb') as file:
        #     idx = pickle.load(file)
        idx = tok_idx
        # with open(settings.indexed_pages_filename, 'rb') as file:
        #     pgs = pickle.load(file)
        pgs = page_idx
        
        response = {'tokens': idx, 'pages': pgs}
        self.send_json(response)
    
    def do_GET_index_search_by_substr(self, paramstr: str):
        '''Searches index for substrings in keys
        
        Search substrings with "q=substr[+more+substrings]"'''
        
        # with open(settings.index_filename, 'rb') as file:
        #     idx = pickle.load(file)
        idx = tok_idx
        # with open(settings.indexed_pages_filename, 'rb') as file:
        #     pgs = pickle.load(file)
        pgs = page_idx

        q_param = self.get_parameter('q', paramstr)
        if q_param is None:
            self.send_error(400, explain='Expected query parameter, e.g. ?q=example')
            return
        
        # '+' denotes spaces: "test string" => "test+string"
        # for queries without '+' split('+') will return a list with one item: the original string
        substrs = q_param.split('+')
        sidx = dict([item for item in idx.items() for sstr in substrs if sstr in item[0]])
            # list comprehensions are nice
            # Basically: filters the index for words which contain any of the substrings in substrs
            #  and makes a new (reduced) dict to return, which is faster than a for loop
        spgs = dict()
        for token, pages in sidx.items():
            for page in pages:
                spgs[page['id']] = pgs[page['id']]
        
        response = {'tokens': sidx, 'pages': spgs}
        self.send_json(response)

    def do_GET_index_search_by_initials(self, paramstr: str):
        '''Searches index by words initials
        
        Search with "q=[char o chars]", e.g. q=apb'''
        
        # with open(settings.index_filename, 'rb') as file:
        #     idx = pickle.load(file)
        idx = tok_idx
        # with open(settings.indexed_pages_filename, 'rb') as file:
        #     pgs = pickle.load(file)
        pgs = page_idx

        q_param = self.get_parameter('q', paramstr)
        if q_param is None:
            self.send_error(400, explain='Expected query parameter, e.g. ?q=exmpl')
            return
        
        sidx = dict([item for item in idx.items() if item[0][0] in q_param])
        spgs = dict()
        for token, pages in sidx.items():
            for page in pages:
                spgs[page['id']] = pgs[page['id']]

        response = {'tokens': sidx, 'pages': spgs}
        self.send_json(response)
    
    def do_GET_index_search_by_stsubstr(self, paramstr: str, send_type='json'):
        '''Searches index for keys starting with the given substrings
        
        Search substrings with "q=substr[+more+substrs]"'''
        
        # with open(settings.index_filename, 'rb') as file:
        #     idx = pickle.load(file)
        idx = tok_idx
        # with open(settings.indexed_pages_filename, 'rb') as file:
        #     pgs = pickle.load(file)
        pgs = page_idx

        q_param = self.get_parameter('q', paramstr)
        if q_param is None:
            self.send_error(400, explain='Expected query parameter, e.g. ?q=example')
            return
        
        # '+' denotes spaces: "test+string" => "test string"
        # for queries without '+' split('+') will return a list with one item: the original string
        substrs = q_param.split('+')
        sidx = dict([item for item in idx.items() for sstr in substrs if item[0].startswith(sstr)])
        spgs = {}
        for token, pages in sidx.items():
            for id in pages:
                spgs[id] = pgs[id]
        
        response = {'tokens': sidx, 'pages': spgs}
        if send_type == 'deflate':
            self.send_compressed_json(response)
        elif send_type == 'pickle':
            self.send_binary(response)
        elif send_type == 'json':
            self.send_json(response)

    def do_GET_index_search_by_literal(self, paramstr: str, send_type='json'):
        '''Searches index for exact matches, and returns pages with all words in their text
        
        Search literals with "q=word[+more+words]"'''
        
        # with open(settings.index_filename, 'rb') as file:
        #     idx = pickle.load(file)
        idx = tok_idx
        # with open(settings.indexed_pages_filename, 'rb') as file:
        #     pgs = pickle.load(file)
        pgs = page_idx

        q_param = self.get_parameter('q', paramstr)
        if q_param is None:
            self.send_error(400, explain='Expected query parameter, e.g. ?q=example')
            return
        
        # '+' denotes spaces: "test+string" => "test string"
        # for queries without '+' split('+') will return a list with one item: the original string
        words = q_param.split('+')
        sidx = dict([item for item in idx.items() for word in words if item[0] == word])
        spgs = {}
        for token, pages in sidx.items():
            for id in pages:
                good = True
                for word in words:
                    if good and word not in pgs[id]['content']:
                        good = False
                if good: spgs[id] = pgs[id]
        
        response = {'tokens': sidx, 'pages': spgs}
        if send_type == 'deflate':
            self.send_compressed_json(response)
        elif send_type == 'pickle':
            self.send_binary(response)
        elif send_type == 'json':
            self.send_json(response)

    def do_GET_help(self):
        '''Help page'''
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Help</title></head>", "utf-8"))
        self.wfile.write(bytes("<body style=\"background-color:#1d1f21\">", "utf-8"))
        self.wfile.write(bytes("<p style=\"color:#c5c8c6\">", "utf-8"))
        self.wfile.write(bytes("GET requests:<br>", "utf-8"))
        self.wfile.write(bytes("&emsp;/full<br>&emsp;&emsp;json<br>", "utf-8"))
        self.wfile.write(bytes("&emsp;&emsp;Returns the entire index.<br>&emsp;&emsp;Very slow, only for testing.<br><br>", "utf-8"))
        self.wfile.write(bytes("&emsp;/subs<br>&emsp;&emsp;json<br>", "utf-8"))
        self.wfile.write(bytes("&emsp;&emsp;Searches index for substrings, returns matching words.<br><br>", "utf-8"))
        self.wfile.write(bytes("&emsp;&emsp;Parameters:<br>", "utf-8"))
        self.wfile.write(bytes("&emsp;&emsp;&emsp;q=search[+more+words]<br><br>", "utf-8"))
        self.wfile.write(bytes("&emsp;/i<br>&emsp;&emsp;json<br>", "utf-8"))
        self.wfile.write(bytes("&emsp;&emsp;Searches index by initial characters.<br>&emsp;&emsp;Slow, but better than /full<br><br>", "utf-8"))
        self.wfile.write(bytes("&emsp;&emsp;Parameters:<br>", "utf-8"))
        self.wfile.write(bytes("&emsp;&emsp;&emsp;q=a[bcd]<br><br>", "utf-8"))
        self.wfile.write(bytes("&emsp;/st<br>&emsp;&emsp;json<br>", "utf-8"))
        self.wfile.write(bytes("&emsp;&emsp;Searches index for substrings, returns words that start with them. Could probably be filtered at endpoint from /subs<br><br>", "utf-8"))
        self.wfile.write(bytes("&emsp;&emsp;Parameters:<br>", "utf-8"))
        self.wfile.write(bytes("&emsp;&emsp;&emsp;q=sear[+more+word]<br><br>", "utf-8"))
        self.wfile.write(bytes("&emsp;/help<br>&emsp;&emsp;html<br>", "utf-8"))
        self.wfile.write(bytes("&emsp;&emsp;This page.<br><br>", "utf-8"))
        self.wfile.write(bytes("Parameters:<br>", "utf-8"))
        self.wfile.write(bytes("&emsp;/path?key=value&key1=value1", "utf-8"))
        self.wfile.write(bytes("</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
    
    def get_parameter(self, param: str, paramstr: str):
        '''Returns the value for the requested parameter, None if not found.
        
        Example paramstr: "<key>=<value>&<key1>=<value1>"'''
        
        params = paramstr.split('&')
        
        try:
            for p in params:
                key, value = p.split('=')
                if key == param:
                    return value
            return None
        except ValueError:
            return None

def start_server(index_fn: str = None, be_quiet: bool = False):
    global quiet 
    quiet = be_quiet

    global tok_idx
    global page_idx
    
    # Load indices, they will be in memory
    try:
        with open(settings.index_filename, 'rb') as fd:
            tok_idx = pickle.load(fd)
        print(f"Word index '{settings.index_filename}' used")
    except FileNotFoundError:
        print(f"Index file at {settings.index_filename} not found.\nAborted", file=sys.stderr)
        exit(1)
    
    try:
        with open(settings.indexed_pages_filename, 'rb') as fd:
            page_idx = pickle.load(fd)
        print(f"Page index '{settings.indexed_pages_filename}' used")
    except FileNotFoundError:
        print(f"Index file at {settings.indexed_pages_filename} not found.\nAborted", file=sys.stderr)
        exit(1)
        
    webServer = HTTPServer((settings.host_name, settings.server_port), IndexServer)
    
    # Terminate process with SIGINT and SIGTERM
    def stop_server(*args):
        webServer.server_close()
        print("Server stopped.")
        exit(0)
    signal(SIGTERM, stop_server)
    
    print("Server started http://%s:%s" % (settings.host_name, settings.server_port))
    print("PID: {}".format(os.getpid()))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt: # SIGINT
        stop_server()

if __name__ == "__main__":
    start_server()
    