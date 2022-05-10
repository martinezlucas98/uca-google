from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import pickle

host_name = "localhost"
server_port = 8080
index_filename = "index/test_indices/large.pickle"

class IndexServer(BaseHTTPRequestHandler):
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
        elif pathstring == '/help':
            self.do_GET_help()
            return
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Top text</title></head>", "utf-8"))
        self.wfile.write(bytes("<p style=\"color:#c5c8c6\">Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body style=\"background-color:#1d1f21\">", "utf-8"))
        self.wfile.write(bytes("<p style=\"color:#c5c8c6\">This request returns nothing. <a href=\"http://{}:{}/help\">Help</a></p>".format(host_name, server_port), "utf-8"))
        self.wfile.write(bytes("<p style=\"color:#c5c8c6\">Bottom text</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
    
    def do_GET_index(self):
        '''Inefficient!
        Returns whole index as json.'''
        with open(index_filename, 'rb') as file:
            idx = pickle.load(file)
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes('%s' % json.dumps(idx, indent=4), "utf-8"))
    
    def do_GET_index_search_by_substr(self, paramstr: str):
        '''Searches index for substrings in keys
        
        Search substrings with "q=substr[+more+substrings]"'''
        
        with open(index_filename, 'rb') as file:
            idx = pickle.load(file)

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
            #  and makes a new (reduced) dict to return, which is faster than 
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes('%s' % json.dumps(sidx, indent=4), "utf-8"))

    def do_GET_index_search_by_initials(self, paramstr: str):
        '''Searches index by words initials
        
        Search with "q=[char o chars]", e.g. q=apb'''
        
        with open(index_filename, 'rb') as file:
            idx = pickle.load(file)

        q_param = self.get_parameter('q', paramstr)
        if q_param is None:
            self.send_error(400, explain='Expected query parameter, e.g. ?q=exmpl')
            return
        
        sidx = dict([item for item in idx.items() if item[0][0] in q_param])
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes('%s' % json.dumps(sidx, indent=4), "utf-8"))
    
    def do_GET_index_search_by_stsubstr(self, paramstr: str):
        '''Searches index for keys starting with the given substrings
        
        Search substrings with "q=substr[+more+substrs]"'''
        
        with open(index_filename, 'rb') as file:
            idx = pickle.load(file)

        q_param = self.get_parameter('q', paramstr)
        if q_param is None:
            self.send_error(400, explain='Expected query parameter, e.g. ?q=example')
            return
        
        # '+' denotes spaces: "test string" => "test+string"
        # for queries without '+' split('+') will return a list with one item: the original string
        substrs = q_param.split('+')
        sidx = dict([item for item in idx.items() for sstr in substrs if item[0].startswith(sstr)])
            # list comprehensions are nice
            # Basically: filters the index for words which contain any of the substrings in substrs
            #  and makes a new (reduced) dict to return, which is faster than 
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes('%s' % json.dumps(sidx, indent=4), "utf-8"))

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
        
        Example paramstr: "key=value&key1=value1"'''
        
        params = paramstr.split('&')
        
        try:
            for p in params:
                key, value = p.split('=')
                if key == param:
                    return value
            return None
        except ValueError:
            return None

if __name__ == "__main__":
    webServer = HTTPServer((host_name, server_port), IndexServer)
    print("Server started http://%s:%s" % (host_name, server_port))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")


''' # Requests example (pip install requests)
import requests

r = requests.get('http://localhost:8080/st?q=query')
if r.status_code == 200:
    index = r.json()
    print(type(index))
    print(index)
    print()
    for token in list(index.keys()):
        print(token + ':')
        for item in index[token]:
            print("    {}: {}".format(item['url'], item['count']))
'''