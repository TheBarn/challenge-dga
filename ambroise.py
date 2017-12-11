# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 15:04:39 2017
@author: Ambroise Prevel
"""

from whoosh.fields import Schema, TEXT, ID
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, FuzzyTermPlugin

def search_in_index(search_kw, index):
    parser = MultifieldParser(["content", "title"], index.schema)
    parser.add_plugin(FuzzyTermPlugin()) 
    searcher = index.searcher()
    to_parse = ' '.join([i+'~0' for i in search_kw.split(' ')]) 
    myquery = parser.parse(to_parse)
    r = searcher.search(myquery)
    results = []
    for res in r:
        results.append(res['path'])
    corrector = searcher.corrector("content")
    suggestions = []    
    for kw in search_kw.split(' '):
        suggestions.append(corrector.suggest(kw))
    searcher.close() 
    return results, suggestions
