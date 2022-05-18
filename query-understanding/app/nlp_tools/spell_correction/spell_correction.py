"""Spelling Corrector in Python 3; see http://norvig.com/spell-correct.html

Copyright (c) 2007-2016 Peter Norvig
MIT license: www.opensource.org/licenses/mit-license.php
"""

################ Spelling Corrector 

import re
import json
from collections import Counter
import pickle
import os






def load_spanish_model() -> Counter:
    with open('app/nlp_tools/spell_correction/spanish_model_WORDS_pkl', 'rb') as f:
        words_obj = pickle.load(f)
    
    return words_obj

def create_and_save_spanish_model() -> Counter:
    # Save the training data file (json) in a dict variable
    training_data_dict = {}
    with open("app/dataset/training_data_spanish.json", "r") as json_file:
        training_data_dict = json.load(json_file)

    words_obj = Counter(training_data_dict) # aca cambie
    with open('app/nlp_tools/spell_correction/spanish_model_WORDS_pkl', 'wb') as f:
        pickle.dump(words_obj, f)

    return words_obj # is a type of COUNTER

WORDS = None

# if the file of the model exists in disk 
# THEN  load the model 
# ELSE create the model, save it in disk and return.
# Both function return a collection.Counter Object
if os.path.exists('app/nlp_tools/spell_correction/spanish_model_WORDS_pkl'):
    WORDS = load_spanish_model() 
else:
    WORDS = create_and_save_spanish_model()
    



def words(text): return re.findall(r'\w+', text.lower())






def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

################ Test Code 

def unit_tests():
    assert correction('masre') == 'madre'              # insert
    assert correction('facuktad') == 'facultad'           # replace 2
    assert correction('bizicleta') == 'bicicleta'               # replace
    assert correction('orarios') == 'horarios'       # insert 2
    assert correction('arrainged') == 'arranged'            # delete
    assert correction('peotry') =='poetry'                  # transpose
    assert correction('peotryy') =='poetry'                 # transpose + delete
    assert correction('word') == 'word'                     # known
    assert correction('quintessential') == 'quintessential' # unknown
    assert words('This is a TEST.') == ['this', 'is', 'a', 'test']
    assert Counter(words('This is a test. 123; A TEST this is.')) == (
           Counter({'123': 1, 'a': 2, 'is': 2, 'test': 2, 'this': 2}))
    # assert len(WORDS) == 32192
    # assert sum(WORDS.values()) == 1115504
    assert WORDS.most_common(10) == [
     ('de', 9999518 ),
     ('la', 6277560),
     ('que', 4681839),
     ('el', 4569652),
     ('en', 4234281),
     ('y', 4180279),
     ('a', 3260939),
     ('los', 2618657),
     ('se', 2022514),
     ('del', 1857225)]
    assert WORDS['the'] == 79808
    assert P('quintessential') == 0
    assert 0.07 < P('the') < 0.08
    return 'unit_tests pass'

def spelltest(tests, verbose=False):
    "Run correction(wrong) on all (right, wrong) pairs; report results."
    import time
    start = time.clock()
    good, unknown = 0, 0
    n = len(tests)
    for right, wrong in tests:
        w = correction(wrong)
        good += (w == right)
        if w != right:
            unknown += (right not in WORDS)
            if verbose:
                print('correction({}) => {} ({}); expected {} ({})'
                      .format(wrong, w, WORDS[w], right, WORDS[right]))
    dt = time.clock() - start
    print('{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second '
          .format(good / n, n, unknown / n, n / dt))
    
def Testset(lines):
    "Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs."
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in lines)
            for wrong in wrongs.split()]

if __name__ == '__main__':
    

    # print(unit_tests())
    # spelltest(Testset(open('spell-testset1.txt')))
    # spelltest(Testset(open('spell-testset2.txt')))
    print(correction('mierianda'))
    print(correction('ke'))
    print(correction('si'))

    