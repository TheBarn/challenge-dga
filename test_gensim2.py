#authors pdespres, fbabin

import numpy
import os
import subprocess
import re
from os import listdir
from os.path import isfile, join
import fnmatch
from nltk.corpus import stopwords
from gensim import corpora, models
from collections import defaultdict

files = []
docNames = {}
i = 0
for root, dirnames, filenames in os.walk('./test_files'):
    for filename in fnmatch.filter(filenames, '*.txt'):
        files.append(os.path.join(root, filename))
#        docNames.append(os.path.join(root, filename))
        docNames[i] = os.path.join(root, filename)
        i += 1

numpy.save('index_dict.npy', docNames)
contractions = re.compile(r"'|-|\"")
# all non alphanumeric
symbols = re.compile(r'(\W+)', re.U)
# single character removal
singles = re.compile(r'(\s\S\s)', re.I|re.U)
# separators (any whitespace)
seps = re.compile(r'\s+')

# cleaner (order matters)
def clean(text):
    text = text.lower()
    text = contractions.sub('', text)
    text = symbols.sub(r' \1 ', text)
    text = singles.sub(' ', text)
    text = seps.sub(' ', text)
    return text

raw_corpus = []
for e in files:
    with open(e) as f:
        str = ""
        for line in f:
            str += clean(line)
        raw_corpus.append(str)

stoplist = set(stopwords.words('english')).union(set(stopwords.words('french')))
texts = [[word for word in document.split() if word not in stoplist]
    for document in raw_corpus]

# Count word frequencies
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

# Only keep words that appear more than once
processed_corpus = [[token for token in text if frequency[token] > 1] for text in texts]

dictionary = corpora.Dictionary(processed_corpus)
dictionary.save('simul.dict')

corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('simul.mm', corpus)

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=300)
corpus_lsi = lsi[corpus_tfidf]
lsi.save('model.lsi')
