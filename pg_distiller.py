# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 05:03:38 2016

Prepping the system:

https://pypi.python.org/pypi/Gutenberg
Had to manually unzip Gutenberg folder to Python27/libs directory Gutenberg 0.4.2
pip install rdflib
pip install future --upgrade


http://www.nltk.org/book/ch03.html
pip install nltk
>>> import nltk
>>> nltk.download()

@author: Wesely
"""

from __future__ import division  # Python 2 users only
import nltk, re, pprint, gzip
from nltk import word_tokenize
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
# http://www.nltk.org/book/ch03.html

def histogram(s):
    d = dict()
    for c in s:
        if c not in d:
            d[c] = 1
        else:
            d[c] += 1
    return d

def get_gutenberg_text(doc_id):
    text = ''
    if doc_id:
        #check if text is already downloaded
        try:
            with gzip.open('archive/{}.txt.gz'.format(doc_id),'rb') as archived_txt:
                print('Loading saved file...')
                text = archived_txt.read().decode('utf-8')
        except:
            print('Downloading text...')
            try:
                text = strip_headers(load_etext(doc_id))
            except:
                print('Unable to download the text.')                    
            if text:
                with gzip.open('archive/{}.txt.gz'.format(doc_id),'wb') as saved_txt:
                    saved_txt.write(text.encode('utf-8'))
    return re.sub(r'[ _\n\r]+',' ',text).strip()

def get_best_sentence(text):
    max_len = 120
    #print(text)
    
    tokens = word_tokenize(text)
    word_frequency = histogram(tokens)
    """
    word_ranks = dict()
    i = 0
    for word in sorted(word_frequency, key=word_frequency.get):
        #print(i)
        word_ranks[word] = i
        i += 1
    """
    for word in word_frequency:
        #nullify small words, no need for its and ands
        if len(word) < 4:
            word_frequency[word] = 0
    #print(word_frequency)
    sents = nltk.sent_tokenize(text)
    max_word_score = 0
    max_score = 0
    max_score_sent = ''
    for sent in sents:
        if len(sent) <= max_len:
            this_score = 0
            words = word_tokenize(sent)
            for word in words:
                if word in word_frequency:
                    this_score += word_frequency[word]
                    if word_frequency[word] > max_word_score:
                        max_word_score = word_frequency[word]
                        print(word,word_frequency[word])
            if this_score > max_score:
                print(this_score)
                max_score = this_score
                max_score_sent = sent
    #pprint.pprint(max_score_sent)
    return max_score_sent
    


#read twitter stream for new PG documents

#download document


#pprint.pprint(sents[79:89])
#844 - importance of being ernest
doc_id = 98

text = get_gutenberg_text(doc_id)
print(get_best_sentence(text))
#Read the document

#find most common words

#find highest ranking sentance under 120 chars

#post the sentance

#zip and delete the book