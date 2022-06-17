import requests
import json
import zlib
import time
import pickle

t0 = time.time()
r = requests.get('http://localhost:8080/st?q=sacerdote+espanol&nolink=1&f=or')
if r.status_code == 200:
    robj = r.json()
    index = robj['tokens']
    page_index = robj['pages']
dt = time.time() - t0
print("Plain text json: time = {} s".format(dt.__round__(4)))
print("                space = {} MB".format((len(r.content) / 1048576).__round__(2)))

t0 = time.time()
r = requests.get('http://localhost:8080/stc?q=sacerdote+espanol&nolink=1&f=or')
if r.status_code == 200:
    robj = json.loads(zlib.decompress(r.content))
    index = robj['tokens']
    page_index = robj['pages']
dt = time.time() - t0
print("Compressed json: time = {} s".format(dt.__round__(4)))
print("                space = {} MB".format((len(r.content) / 1048576).__round__(2)))

t0 = time.time()
r = requests.get('http://localhost:8080/sts?q=sacerdote+espanol&nolink=1&f=or')
if r.status_code == 200:
    robj = pickle.loads(r.content)
    # index = robj['tokens']
    # page_index = robj['pages']
dt = time.time() - t0
print("Pickled dict:    time = {} s".format(dt.__round__(4)))
print("                space = {} MB".format((len(r.content) / 1048576).__round__(2)))
